speciality = ['surgeon', 'nurse', 'lawyer', 'accountant', 'marketing', 'engineer', 'finance', 'software', 'physical+therapist', 'architect']
city = ['Austin', 'Dallas', 'McAllen', 'San+Antonio', 'Houston', 'Brownsville', 'El+Paso']
state = "Texas"
holding = []
for i in range(len(speciality)): 
    for p in range(len(city)):
        url = "https://www.yellowpages.com/search?search_terms=" + speciality[i] + "&geo_location_terms=" + city[p] + "%2C+" + state
        holding.append(url)