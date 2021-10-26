If you look at the _Heatmaps_ page, you'll see that my `sleep` doesn't really conform to your typical sleeping schedule. This goes for every time variable I track &ndash; while each day in the Excel sheet starts at 00:00 and ends at 23:59, that's not when the day starts and ends _for me_.
The day starts whenever I wake up, and ends whenever I go to sleep (ignoring naps). This distors the data. Say I wake up at 10am on Tuesday and go to sleep at 2am on Wednesday. Whatever I did between 00:00 and 02:00 will logically be labeled as Wednesday data, but practically, that time period was still Tuesday for me.
The same applies any time I don't go to sleep at exactly 00:00 on two consecutive days (perfect time separation of a single day), which happens all the time.

### Solution (?)

For practically all visualization and models here, I'll be using what I call _segmented_ data &ndash; the day starts when I wake up, and ends when I go to sleep.

- Example: I wake up (hypothetically) at 4pm on Saturday. I am awake for 16 hours, meaning I go to sleep at 8am on Sunday. The data about whatever I spent my time on during those 16 hours will belong to the row for Saturday.

- Here you can see a comparison of the original and segmented structure of time data for one week (`grey color=sleep`):
