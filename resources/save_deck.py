import requests
import re
from xml.dom.minidom import Document

def fetch_and_parse_json(url, path):
	"""
	Fetch Moxfield Deck as JSON data and save it as a Cockatrice deck file.

	Args:
		url (str): The URL to fetch JSON data from.
		path (str): Folder to store decks in

	Returns:
		Name of created file
	"""

	# Request JSON
	response = requests.get(url)

	# Check for request errors
	response.raise_for_status()

	# Parse JSON
	json_data = response.json()

	# Create xml document
	document = Document()

	# Create the XML structure

	# Create deck
	deck = document.createElement("cockatrice_deck")
	deck.setAttribute("version", "1")
	document.appendChild(deck)

	# Creeate deck name
	deckname = document.createElement("deckname")
	deckname.appendChild(document.createTextNode(json_data["name"]))
	deck.appendChild(deckname)

	# Create description
	comments = document.createElement("comments")
	description = json_data["description"]
	commanders = json_data["boards"]["commanders"]["cards"].items()
	if len(description) > 0 :
		description += "\n\n"
	if len(commanders) == 1 :
		description += "Commander:\n"
	elif len(commanders) > 1 :
		description += "Commanders:\n"
	for card_id, card_info in commanders :
		description += f"{card_info["card"]["name"]}\n"
	if len(description) > 0 :
		description += "\n"
	description += f"Author: {json_data["createdByUser"]["userName"]}\nLink: moxfield.com/decks/{json_data["publicId"]}"
	comments.appendChild(document.createTextNode(description))
	deck.appendChild(comments)

	# Create main zone
	main_zone = document.createElement("zone")
	main_zone.setAttribute("name", "main")
	deck.appendChild(main_zone)

	# Add commanders and mainboard cards to main zone
	for board in ["commanders", "mainboard"]:
		for card_id, card_info in json_data["boards"][board]["cards"].items():
			card = document.createElement("card")
			card.setAttribute("number", str(card_info["quantity"]))
			card.setAttribute("name", card_info["card"]["name"])
			main_zone.appendChild(card)

	# Create tokens zone
	tokens_zone = document.createElement("zone")
	tokens_zone.setAttribute("name", "tokens")
	deck.appendChild(tokens_zone)

	# Add tokens to tokens zone
	for token in json_data["tokens"]:
		card = document.createElement("card")
		card.setAttribute("number", "1")
		card.setAttribute("name", token["name"])
		tokens_zone.appendChild(card)

	# Regex pattern for invalid characters for filename
	pattern = r"[\\\/:\*\?\"<>|]"
	# Create filename
	xml_file_name = f"{json_data["name"]} [{json_data["publicId"]}].cod"
	# Clean filename of invalid characters and concatenate path
	xml_file_name = path +  re.sub(pattern, "", xml_file_name)
	# Write file
	with open(xml_file_name, "w", encoding="utf-8") as xml_file:
		pretty = document.toprettyxml(indent="    ")
		xml_file.write(pretty)

	print(f"XML file created: {xml_file_name}")

	return xml_file_name
