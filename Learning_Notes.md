# Learning Notes

Apuntes personales sobre conceptos de este proyecto que vale la pena poder
explicar sin sonar memorizados (ver "Understand-before-copy" en `CLAUDE.md`).
Cada entrada queda fechada porque el código puede cambiar después.

---

## 2026-09-16 — Cómo funcionan las fixtures de `conftest.py`

Contexto: `conftest.py` tiene tres fixtures — `driver`, `products_in_cart` y
`checkout_step_one` — que varios tests en `test_cart.py` y `test_checkout.py`
usan como parámetros. Esto es lo que realmente pasa cuando corre un test.

### La idea base: pytest hace "inyección de dependencias" por nombre

Un fixture es una función marcada con `@pytest.fixture()`. Pytest mira los
**parámetros que un test pide en su firma** y busca un fixture con ese mismo
nombre para dárselo — no hay ningún `import` de por medio, es *matching* por
nombre de string.

Por eso `driver` funciona en todos los tests sin nunca hacer
`from conftest import driver`: cuando un test tiene `def test_algo(driver):`,
pytest ve el parámetro `driver`, busca una función `def driver(...)` decorada
con `@pytest.fixture()`, la ejecuta, y lo que esa función devuelve (o
`yield`ea) es lo que llega como el argumento `driver` al test. Esto funciona
automáticamente solo porque está en `conftest.py` — es el archivo que pytest
escanea especialmente en cada carpeta para descubrir fixtures compartidos.

### `return` vs `yield`: setup solo, o setup + teardown

`driver` usa `yield`:

```python
driver.maximize_window()
driver.get(BASE_URL)
yield driver          # <- el test corre ACÁ, con driver = esto
driver.quit()         # <- esto corre DESPUÉS de que el test termina (pase o falle)
```

Todo lo de antes del `yield` es el "arrange"; todo lo de después es la
limpieza garantizada (corre incluso si el test falla).

`products_in_cart` y `checkout_step_one` usan `return` en vez de `yield`,
porque no necesitan limpiar nada después — el `driver.quit()` de la fixture
`driver` ya se encarga de cerrar el browser al final.

### Fixtures que dependen de otras fixtures

```python
@pytest.fixture()
def products_in_cart(driver):   # <- pide "driver" como parámetro
    ...
    return TWO_PRODUCTS

@pytest.fixture()
def checkout_step_one(driver, products_in_cart):   # <- pide dos fixtures
    ...
    return products_in_cart
```

Un fixture puede pedir OTRO fixture como parámetro, igual que un test.
Pytest resuelve esto como un grafo de dependencias.

### Trazando un ejemplo real: `test_missing_first_name(driver, checkout_step_one)`

1. Se ejecuta `driver` → abre Chrome headless, hace `.get(BASE_URL)`, y
   "pausa" en el `yield` entregando el objeto `driver`.
2. Se ejecuta `products_in_cart(driver)` → usa ESE MISMO objeto `driver`
   (dentro de un mismo test, todos los fixtures que pidan `driver` reciben
   la misma instancia), hace login, agrega los 2 productos, devuelve
   `TWO_PRODUCTS`.
3. Se ejecuta `checkout_step_one(driver, products_in_cart)` → recibe el
   `driver` del paso 1 y la lista del paso 2, navega a carrito → checkout,
   devuelve la misma lista.
4. Corre el cuerpo del test, con `driver` ya logueado y en checkout-step-one.
5. Al terminar el test, se reanuda el `yield` de `driver`: corre
   `driver.quit()`.

### Punto importante: esto no reusa un browser entre tests

El fixture `driver` es *function-scoped* por default (el scope que no se
especifica), así que todo el proceso se repite — browser nuevo, login nuevo,
agregar productos de nuevo — para cada test que lo use. Lo que se gana acá
no es velocidad, es no tener que **escribir** las mismas líneas de setup en
cada test. Cada test sigue corriendo aislado e independiente del resto, que
es justo lo que se quiere en tests de UI (que un test no dependa del estado
que dejó otro).

---

## 2026-09-16 — Por qué algunos clics usan `execute_script` en vez de `.click()`

Contexto: en `cart_page.py`, `inventory_page.py`, `checkout_page.py` y
`product_page.py` hay métodos que, en vez de hacer `elemento.click()` como
uno esperaría, hacen esto:

```python
self.driver.execute_script("arguments[0].click();", elemento)
```

Esto no es una preferencia de estilo — es la solución a un bug real que
encontramos, así que vale la pena entender el problema antes que la solución.

### El problema: un clic que "funciona" pero no hace nada

`elemento.click()` le pide a Selenium que simule un clic de mouse real: calcula
en qué posición de la pantalla está el elemento y le dice al navegador "hacé
clic ahí", como si fuera un dedo tocando la pantalla en esas coordenadas.

Para que un navegador entregue ese clic simulado al elemento correcto, la
ventana/pestaña tiene que tener **foco** — tiene que ser la ventana "activa"
en ese momento, igual que en tu compu si tenés dos ventanas abiertas y hacés
clic en una que no está al frente, a veces el primer clic solo activa la
ventana y no llega a tocar el botón de adentro.

Corriendo los tests en Chrome **headless** (sin ventana visible, como corren
en CI y como los corremos acá para no abrir un browser en pantalla), notamos
algo raro: a veces `elemento.click()` no tiraba ningún error, pero la página
se quedaba exactamente igual — como si el clic nunca hubiera pasado. Eso es
mucho más confuso que un error, porque el código "no falla", pero el test
sí, con un mensaje que no tiene nada que ver con clics (por ejemplo,
"encontré 6 productos en vez de 2").

### Cómo lo confirmamos (no lo asumimos)

Metimos un chequeo de diagnóstico justo antes del clic problemático:

```python
print(self.driver.execute_script("return document.hasFocus()"))
```

`document.hasFocus()` es una función de JavaScript que devuelve `True` si esa
pestaña es la que tiene el foco en ese momento. Nos dio `False` justo antes
de los clics que "no hacían nada" — confirmando que el clic se estaba
perdiendo por falta de foco, típico de correr un browser sin ventana.

Nos pasaba sobre todo en dos situaciones:
- La página llevaba un rato sin actividad (~10 segundos o más).
- Se hacía un clic justo después de otro clic o de una navegación (por
  ejemplo, click_item justo después de continue_shopping).

### La solución: pedirle al DOM que haga clic, no al mouse

En vez de simular un clic físico (que depende del foco de la ventana),
`execute_script("arguments[0].click();", elemento)` le dice al navegador:
"ejecutá directamente el método `.click()` de JavaScript que tiene este
elemento" — es lo mismo que escribir `elemento.click()` en la consola del
navegador. Esto dispara los mismos event listeners que un clic real (el botón
"reacciona" igual), pero no depende de que la ventana tenga foco, porque no
hay ningún evento de mouse de por medio — es una llamada directa a una
función del propio elemento.

`arguments[0]` es cómo `execute_script` recibe elementos de Python: el script
que le pasás es JavaScript puro, y `arguments` es un array con los valores
extra que le mandás después del string (acá, un solo elemento: el botón).

### Por qué no se usó en todos lados

Un clic vía JS es un poco menos "realista" que un clic real — no valida que
el elemento sea visible o que no esté tapado por otra cosa, como sí lo hace
un clic de verdad. Por eso solo se aplicó en los métodos que efectivamente
mostraron el problema (o que son candidatos claros porque hacen clic justo
después de otro clic/navegación): `CartPage.remove_item`,
`CartPage.continue_shopping`, `CartPage.go_to_checkout`, `CartPage.click_item`,
`InventoryPage.go_to_cart`, `ProductPage.back_to_products`,
`ProductPage.add_to_cart`, `ProductPage.remove_from_cart`, y
`CheckoutPage.cancel`. `InventoryPage.add_to_cart` se dejó con el clic normal
porque siempre se ejecuta apenas carga la página, antes de cualquier otro
clic, y nunca reprodujo el problema en muchas corridas de prueba.

---

## 2026-09-16 — `StaleElementReferenceException` y por qué a veces se ignora

Contexto: en `cart_page.py`, los métodos `get_item_names` y `click_item`
tienen un patrón raro a primera vista — un `for` que reintenta hasta 3 veces
atrapando una excepción puntual:

```python
def get_item_names(self):
    for _ in range(3):
        try:
            items = self.driver.find_elements(*self.CART_ITEM_NAME)
            return [item.text for item in items]
        except StaleElementReferenceException:
            continue
    return []
```

Y en `remove_item`, la misma excepción se le pasa directamente a
`WebDriverWait`:

```python
WebDriverWait(
    self.driver, 5, ignored_exceptions=(StaleElementReferenceException,)
).until(...)
```

### Qué es un elemento "stale" (obsoleto)

Cuando hacés `driver.find_element(...)`, Selenium no te da "el botón que
dice Remove" en abstracto — te da una referencia a un nodo específico del
DOM, tal como existía en ese instante exacto.

El problema es que muchas páginas modernas (esta incluida) vuelven a dibujar
partes de la pantalla con JavaScript incluso cuando visualmente no cambia
nada — por ejemplo, justo después de cargar la página del carrito. Cuando
eso pasa, el navegador puede destruir el nodo viejo y crear uno nuevo que se
ve idéntico, pero que técnicamente es un objeto distinto. Tu referencia
vieja queda apuntando a un nodo que ya no existe: "stale" (obsoleta).

Si intentás usar esa referencia vieja (leer su `.text`, hacer `.click()`),
Selenium tira `StaleElementReferenceException`. No es un error de tu lógica
— es una carrera contra el re-renderizado de la página, y a veces perdés esa
carrera.

### La solución 1: reintentar manualmente

El patrón `for _ in range(3): try / except StaleElementReferenceException:
continue` dice, en criollo: "intentá leer los elementos; si se volvieron
obsoletos justo mientras los leía, no pasa nada, probá de nuevo (hasta 3
veces) — probablemente para el segundo intento el re-render ya terminó".

### La solución 2: decirle a `WebDriverWait` que la ignore

`WebDriverWait` normalmente reintenta su condición cada medio segundo, pero
si esa condición tira una excepción que no esperaba, se rinde al toque en
vez de seguir reintentando. `ignored_exceptions=(StaleElementReferenceException,)`
le dice "si te encontrás con ESTA excepción puntual mientras esperás, no la
trates como un fallo — tratala como 'todavía no está listo' y seguí
reintentando hasta que se cumpla el timeout". Es una forma más prolija de
lograr lo mismo que el `for`/`try`/`except`, cuando ya estás usando
`WebDriverWait` de todos modos.

---

## 2026-09-16 — El parámetro `submit` en `fill_info` (un truco chico pero útil)

Contexto: `CheckoutPage.fill_info(first_name, last_name, postal_code, submit=True)`
ahora acepta un cuarto parámetro opcional.

Antes, `fill_info` siempre llenaba el formulario Y apretaba "Continue" en el
mismo método. Eso rompía `test_cancel_mid_checkout`: el test necesitaba
llenar el formulario pero NO avanzar, para después cancelar desde el primer
paso del checkout (que vuelve al carrito) en vez del segundo paso (que —
descubrimos probando a mano — te manda al catálogo de productos, no al
carrito).

En vez de escribir un segundo método casi idéntico (`fill_info_sin_submit`,
duplicando las mismas 10 líneas), se agregó un parámetro booleano con un
valor por default que no rompe a nadie que ya lo estuviera usando:

```python
def fill_info(self, first_name, last_name, postal_code, submit=True):
    ...
    if submit:
        # clic en Continue
```

Cualquier test viejo que llame `fill_info(...)` sin el cuarto argumento
sigue funcionando exactamente igual (porque `submit=True` es el default). El
único test que necesita el comportamiento distinto lo pide explícitamente:
`fill_info(..., submit=False)`. Es un patrón común en Page Object Model para
cubrir una variación chica de un flujo sin duplicar código ni crear un método
nuevo por cada variante.
