## Scraper of a kinopoisk unofficial API:movie_camera:

:wave:Hello and Welcome,
<br><br>

### Our branches:

:round_pushpin:**Scraper_v.1.0** — this scraper scraps data from the [Kinopoisk Unofficial API](https://kinopoiskapiunofficial.tech/) in to a .csv file. It not only scraps data but also checks if each movie has a kinopoisk rating and a year. The scraper also converts "Countries" and "Genres" attributes from dictionaries inside lists to just list format, which I prefer more.
This scraper has been created especially for [this](https://github.com/DmitryKorzhIT/Telegram_Main_Bot) Telegram Bot.
<br><br>

:round_pushpin:**Scraper_v.2.0** — the second version of the scraper get the .csv file from the `scrapter_v.1.0` and parse the follow attributes:
- Movie rating votes amount
- Film length
- Rating MPAA
- Rating age limits
- Short description
- Description
<br><br>

:round_pushpin:**Data_Cleaner_v.3.0** — this version cleans data to make it looks almost perfect! It helps to get rid of some unnecessary data and make the data good structured. This data cleaner does the following things:
- Replace the "None" string into "Nan" values
- Merge "Short description" and "Description"
- Remove duplicated movies
- Remove movies with no data about "description" or "Film length"
- Remove movies with the genre "For adult"
- Merge "Rating age limits" with "Rating MPAA"
- Remove unnecessary columns
