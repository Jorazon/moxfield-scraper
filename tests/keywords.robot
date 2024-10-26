*** Settings ***
Library  OperatingSystem
Library  String
Library  RPA.Browser.Selenium

Library  save_deck.py

Variables  variables.py

*** Keywords ***
Store the latest ${number_of_decks} decks
    Open Available Browser  ${DECK_URL}  headless=True
    Store decks  ${number_of_decks}
    [Teardown]  Close Browser

Store decks
    [Arguments]  ${number_of_decks}

    ${deck_locator}=  Get Deck Locator
    ${decks}=  Get WebElements  ${deck_locator}
    ${deck_names}=  Get WebElements  ${deck_locator}/span/span/span/span[2]/span
    ${decks_count}=  Get Length  ${decks}
    ${output_dirmane}=  Get output directory
    Create Directory  ${output_dirmane}

    FOR  ${index}  IN RANGE  1  ${decks_count}
        Exit For Loop If  ${index} > ${number_of_decks}
        ${href}=  Get Element Attribute  ${decks}[${index}]  href
        Store Deck  ${href}  ${output_dirmane}
    END

Get Deck Locator
    [RETURN]  xpath://a[descendant::em[contains(text(), "Commander / EDH")]]

Store Deck
    [Arguments]  ${deck_url}  ${output_dirmane}
    ${deck_id}=  Remove String  ${deck_url}  ${BASE_URL}/decks/
    ${json_url}=  Set Variable  ${MOXFIELD_API_URL}${deck_id}
    ${deck_filename}=  fetch_and_parse_json  ${json_url}  ${output_dirmane}
    [RETURN]

Get output directory
    [RETURN]  ${CURDIR}\\..\\output\\decks\\
