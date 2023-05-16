import os
import dimcli
import csv

# JP's personal API Key was here
dimcli.login(key="", endpoint="https://app.dimensions.ai")

dsl = dimcli.Dsl()

def _getAbstract(id):
	"""Takes a string ID from Dimensions.ai and returns abstract corresponding to ID"""
	res = dsl.query(f"""search publications for \"{id}\" return publications [abstract + journal]""")
	formattedRes = res.json
	abstract = formattedRes['publications'][0]['abstract']
	return abstract

def abstractCSV(ids, csvFileName):
	"""Takes list of string IDs and string of desired CSV fileName. Retrieves abstracts for each ID, and loads them into a CSV file titled {csvFileName} with an index, ID, and Abstract column."""
	with open(csvFileName, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(["", "ID", "Abstract"])
		for i in range(len(ids)):
			abstract = _getAbstract(ids[i])
			writer.writerow([i+1, ids[i], abstract])
	file.close()

# Test case with IDs from 
# 'title':'Tailpipe, resuspended road dust, and brake-wear emission factors from on-road vehicles'
#  ‘id’:’pub.1012273157’
# 'title': 'Relationship of Hydrocarbons to Oxidants in Ambient Atmospheres'
# 'id': 'pub.1034859593'
# 'title':'New and Improved Procedures for Gas Sampling and Analysis in the National Air Sampling Network'
# 'id': 'pub.1029962184'

# abstract CSV example: abstractCSV(["pub.1012273157","pub.1034859593","pub.1029962184"], "TestCriteriaReportIds.csv")


def _getJournal(id):
	"""Takes a string ID from Dimensions.ai and returns abstract corresponding to ID"""
	res = dsl.query(f"""search publications for \"{id}\" return publications [abstract + journal]""")
	formattedRes = res.json
	print("formatted res", formattedRes)
	print(len(formattedRes['publications']))
	if len(formattedRes['publications']) > 0:
		journalId = formattedRes['publications'][0]['journal']['id']
		journalTitle = formattedRes['publications'][0]['journal']['title']	
	else:
		journalId = ""
		journalTitle = ""
	return [journalId, journalTitle]

def journalCSV(ids, csvFileName):
	"""Takes list of string IDs and string of desired CSV fileName. Retrieves abstracts for each ID, and loads them into a CSV file titled {csvFileName} with an index, ID, and Abstract column."""
	with open(csvFileName, 'w') as file:
		writer = csv.writer(file)
		writer.writerow(["", "ID", "Journal ID", "Journal Title"])
		for i in range(len(ids)):
			abstract = _getJournal(ids[i])
			writer.writerow([i+1, ids[i], abstract[0], abstract[1]])
	file.close()

# journal CSV example: journalCSV(["pub.1012273152","pub.1012273153","pub.1012273154","pub.1012273155","pub.1012273156","pub.1012273157","pub.1012273158","pub.1012273159","pub.1012273160","pub.1012273161","pub.1012273162"], "TestJournalIds.csv")

def journalYear(journalName, year, csvFileName):
	"""Takes list of string IDs and string of desired CSV fileName. Retrieves abstracts for each ID, and loads them into a CSV file titled {csvFileName} with an index, ID, and Abstract column."""
	with open(csvFileName, 'w') as file:
		writer = csv.writer(file)
		writer.writerow([""])
		info = _journalYear(journalName, year)
		for obj in range(len(info)):
			row = []
			for key in info[obj].keys():
				row.append(info[obj][key])
			writer.writerow(row)
	file.close()

def _journalYear(journalName, year):
	"""Takes journalName string and year integer and retrieves report information Dimensions.ai and loads information into a CSV"""
	res = dsl.query(f"""set return_all_keys search publications where journal.title = \"{journalName}\" and year = {year} return publications limit 1000""")
	formattedRes = res.json
	publications = formattedRes['publications']
	return publications


# journal year example: journalYear("American Journal of Dermatopathology", 2010, "testJournal2010CSV.csv")