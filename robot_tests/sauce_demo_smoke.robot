*** Settings ***
Resource    common.resource

*** Test Cases ***
Login And Add Backpack To Cart
    Login As Standard User
    Add Backpack To Cart
    Element Text Should Be    class=shopping_cart_badge    1
    [Teardown]    Close Browser
Remove Item From Cart
    Login As Standard User
    Add Backpack To Cart
    Remove Backpack From Cart
    Page Should Not Contain Element     class=shopping_cart_badge
    [Teardown]    Close Browser
Complete Checkout Flow
    Login As Standard User
    Add Backpack To Cart
    Go To Cart
    Go To Checkout
    Fill Checkout Information    Melina    Buslaiman    5000
    Complete Order
    Element Should Contain    class=complete-header    Thank you for your order!
    [Teardown]    Close Browser
Sort Products A To Z
    Login As Standard User
    Sort Products By Name Ascending
    @{actual_names}=    Get All Product Names
    @{expected_names}=    Copy List    ${actual_names}
    Sort List    ${expected_names}
    Lists Should Be Equal    ${actual_names}    ${expected_names}
    [Teardown]    Close Browser
Sort Products Z To A
    Login As Standard User
    Sort Products By Name Descending
    @{actual_names}=    Get All Product Names
    @{expected_names}=    Copy List    ${actual_names}
    Sort List    ${expected_names}
    Reverse List    ${expected_names}
    Lists Should Be Equal    ${actual_names}    ${expected_names}
    [Teardown]    Close Browser