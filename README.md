# Airfare-flights-web-scraping]
<h1> What does this project do?</h1>

<h2> The file: main with classes </h2>
<h3> This program has 4 main functions </h3>
<ol>
  <li> get_token()</li>
  <li> get_data()</li>
  <li> iterate_date()</li>
</ol

  <p><b> What does get_token do? </b></p>
<p> It retrieves the token needed to access the API</p>


<p><b> What does get_data do? </b></p>
<p> It takes the json data given by the Amadeus API and dumps into a json file. The data only covers all of the flights for a single day. </p>


<p><b> What does iterate_date do? </b></p>
<p> It goes over each day of the year, and by implementing get_data(), get that into a json file. </p>
<p> This json file will cover all of the flights throughout the whole year.</p>
<p> Different json files will be used for when the data retrieved is for different <b>origin</b> and <b>departure</b> locations.</p>


<h2> How data analysis is going to work</h2>
<p> There is going to be a different dataframe each time I will have a different origin and destination</p>
<p> Each dataframe will have the index set to the date.</p>
<p> Rows will consist of: </p>
<ul>
  <li> The minimum price of each day</li>
  <li> The currrency of that flight</li>
  <li> The number of stops of that flight(Note: I have to figure out how to get the index of the minimum price of the np.array)</li>
</ul




<h3> Current stage I am at: </h3>

<p> I had been able to satinise the data by creating a dictionary from the json file. </p>
<p>The file includes: the number of stops, the currency and the price of each flight. This is for every single date.</p>
<p> I am now going to create dataframe based on this dictionary that I created.</p>

<p><b> Note to self: when trying to iterate through a column or row of a dataframe, use the apply() or map() method to get advantage of vectorisation</b></p>
<p><b> Note to self: When trying to read json data from a file, do it with 'r' mode because 'w' mode causes isssues</b></p>


<h2> Future plans </h2>
<h3> As of 26/1/2023</h3>
<p> Try to learn how to use multiprocessing to make multiple requests to the API</p>
<p> Optimise code? </p>
<p> Learn more about context managers </p>




