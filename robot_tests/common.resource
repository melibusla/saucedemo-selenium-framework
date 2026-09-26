*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${URL}         https://www.saucedemo.com/
${BROWSER}     chrome
${HEADLESS}    ${TRUE}
${USERNAME}    standard_user
${PASSWORD}    secret_sauce

*** Keywords ***
Open Sauce Demo Browser
    IF    ${HEADLESS}
        Open Browser    ${URL}    ${BROWSER}    options=add_argument("--headless=new")
    ELSE
        Open Browser    ${URL}    ${BROWSER}
    END

Login As Standard User
    Open Sauce Demo Browser
    Input Text    id=user-name    ${USERNAME}
    Input Text    id=password    ${PASSWORD}
    Click Button    id=login-button
    Wait Until Page Contains Element    id=inventory_container

Add Backpack To Cart
    Click Button    id=add-to-cart-sauce-labs-backpack

Remove Backpack from Cart
    Click Button    id=remove-sauce-labs-backpack

Go To Cart
    Click Element    class=shopping_cart_link

Go To Checkout
    Click Button    id=checkout

Fill Checkout Information
    [Arguments]    ${first_name}    ${last_name}    ${zip_code}
    Input Text    id=first-name    ${first_name}
    Input Text    id=last-name    ${last_name}
    Input Text    id=postal-code    ${zip_code}
    Click Button    id=continue

Complete Order
    Click Button    id=finish

Sort Products By Name Ascending
    Select From List By Value    class=product_sort_container    az

Sort Products By Name Descending
    Select From List By Value    class=product_sort_container    za

Get All Product Names
    @{elements}=    Get WebElements    class=inventory_item_name
    @{names}=    Create List
    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        Append To List    ${names}    ${text}
    END
    RETURN    ${names}