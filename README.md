# Airfare-flights-web-scraping]



<h3> Current stage I am at: </h3>

<p> I had been able to satinise the data by creating a dictionary from the json file. </p>
<p>The file includes: the number of stops, the currency and the price of each flight. This is for every single date.</p>
<p> I am now going to create dataframe based on this dictionary that I created.</p>

<p><b> Note to self: when trying to iterate through a column or row of a dataframe, use the apply() or map() method to get advantage of vectorisation</b></p>



<h2> How data analysis is going to work</h2>

<p> There is going to be a different dataframe each time I will have a different origin and destination</p>
<p> Each dataframe will have the index set to the date.</p>
<p> Rows will consist of: </p>
<ul>
  <li> The minimum price of each day</li>
  <li> The currrency of that flight</li>
  <li> The number of stops of that flight</li>
</ul
