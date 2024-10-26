*** Settings ***
Documentation  Web scraper robot. Stores the last updated EDH deck from Moxfield in Cockatrice format.
Variables      variables.py
Resource       keywords.robot

*** Tasks ***
Store the ${NUMBER_OF_DECKS} latest EDH decks
    Store the latest ${NUMBER_OF_DECKS} decks
