Hello!

This is my financial dashboard project,

This project as of this point mainly uses Python, Streamlit, Pandas and plotly express
I used streamlit to host because it was easy to learn and use, and I came across some of their development teams stuff and really wanted to try it out.
Pandas and plotly were used because theyre the main libraries I had experience using in university, and also I didn't plan on needing alot of intricate breakdowns in this version, so i figured the math being utilized was okay.

In this code, i tried to mainly code it myself by following tutorials and googling stuff, and I used A.I to troubleshoot.

I tried to avoid using copilot to code, but I had it autofill in when I was putting search terms in the categorization function.

I dont really have much of a coding background other then a few courses I've taken in university, the most difficult things being data splicing using Eclipse, or making a monte carlo simulation in jupyter,car loan calc in VBA, and things of that nature.

The code works in order of how you see it;




///(Code explained skip if u want)

**Debits = money going out, Credit = Money going in

1, imports

Streamlit hello messages

Page setup

Transaction categorization function (it works by looking for specific keywords in the dataframe we will import later)
then checks to see if there is a value in credit to distinguish if something like the word "pay" would be a cash inflow or outflow

Load function works by having a file being loaded, "dataframe = pd.read_csv" because its a csv,
I make it so it loads without commas for cleaner work,
I name the collumns appropriately,
then do some formatting code, i.e no excess white space, fill in null values with a dash

then categorization function is used to sieve through and organize the data, which is called back to earlier in the program

and if something goes wrong I have it tell me a funny message "ayo we got a file processing error"


Afterwards I have a function which segregates the data into 3 dataframes, and some charts;

I have it setup as the main DF, Cash inflow (credit) DF, and then the Cash outflow (Debit DF)

then some charts to be made and displayed in streamlit, with placeholder for later incase I decide to add some later.

////


**FUTURE**
I plan to add
- Visualization tweaks,
- More charts
- Have it save and compress data into a master file, removing duplicates,
- Suggestions based on inputs
