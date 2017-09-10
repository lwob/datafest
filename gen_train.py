import math
import csv
import collections as c
import datetime
import dateutil.parser


class Empty:
    pass


data_f = open("data_nonull.txt")
data_csv = csv.reader(data_f, delimiter='\t')

col2name = next(data_csv)
h = Empty()
for (i, name) in enumerate(col2name):
    setattr(h, name, i)

data = [_ for _ in data_csv]

col2value2count = c.defaultdict(lambda: c.defaultdict(int))

cmf_to_n = {
    "VC": 0.0,
    "C": 1.0,
    "M": 2.0,
    "F": 3.0,
    "VF": 4.0,
}

lmh_to_n = {
    "VL": 0.0,
    "L": 1.0,
    "M": 2.0,
    "H": 3.0,
    "VH": 4.0,
}

columns = [
    h.date_time,                 # Separate to day-of-week, hour-of-day
    # h.site_name,
    h.user_location_country,
    # h.user_location_region,
    # h.user_location_city,       # Transform to popularity of city
    # h.user_location_latitude,
    # h.user_location_longitude,
    h.orig_destination_distance,
    # h.user_id,
    h.is_mobile,
    h.is_package,
    h.channel,                   # Categorical
    # h.srch_ci,                  # Transform to days_to_booking, drop neg
    # h.srch_co,                  # Transform to duration of stay
    h.srch_adults_cnt,
    h.srch_children_cnt,
    h.srch_rm_cnt,
    # h.srch_destination_id,
    h.hotel_country,             # Transform: Same country? Different?
    h.is_booking,                # Predict this
    # h.hotel_id,
    h.prop_is_branded,
    h.prop_starrating,           # Normalize, drop 0
    h.distance_band,             # Normalize
    h.hist_price_band,           # Normalize
    h.popularity_band,
    h.cnt,
]

categorical = [
    h.user_location_city,
    h.channel,
]

channels = {
    "231": 0,
    "262": 1,
    "293": 2,
    "324": 3,
    "355": 4,
    "386": 5,
    "417": 6,
    "448": 7,
    "479": 8,
    "510": 9,
    "541": 10,
}

channels_lst = [
    "231",
    "262",
    "293",
    "324",
    "355",
    "386",
    "417",
    "448",
    "479",
    "510",
    "541",
]

out_cols = [
    "click_weekday",
    "click_hour",
    "ln_country_popularity",
    "orig_destination_distance",
    "is_mobile",
    "is_package",
] + [
    "chan_" + c for c in channels_lst
] + [
    "days_to_booking",
    "duration_of_stay",
    "srch_adults_cnt",
    "srch_children_cnt",
    "srch_rm_cnt",
    "same_country",
    "prop_is_branded",
    "prop_starrating",
    "distance_band_n",
    "hist_price_band_n",
    "popularity_band_n",
    "cnt",
    #"is_booking",
    "user_id",
    "srch_destination_id",
    "date_time",
    "site_name",
    "user_location_region",
    "user_location_city",
    "user_location_latitude",
    "user_location_longitude",
]

for row in data:
    for col in categorical:
        col2value2count[col][row[col]] += 1

ouf = open("train.txt", 'w', newline='')
out = csv.writer(ouf, delimiter='\t')
out.writerow(out_cols)
for row in data:
    if row[h.is_booking] != '1':
        continue
    click_time = dateutil.parser.parse(row[h.date_time])
    ci_date = datetime.date(*map(int, row[h.srch_ci].split('-')))
    co_date = datetime.date(*map(int, row[h.srch_co].split('-')))
    days_to_booking = (ci_date - click_time.date()).days
    if days_to_booking < 0:
        continue
    duration_of_stay = (co_date - ci_date).days
    row = [
        click_time.weekday(),
        click_time.hour*24+click_time.minute,
        math.log(max(1, col2value2count[h.hotel_country][row[h.hotel_country]])),
        row[h.orig_destination_distance],
        row[h.is_mobile],
        row[h.is_package],
    ] + [
        int(row[h.channel] == i) for i in channels_lst
    ] + [
        days_to_booking,
        duration_of_stay,
        row[h.srch_adults_cnt],
        row[h.srch_children_cnt],
        row[h.srch_rm_cnt],
        int(row[h.hotel_country] == row[h.user_location_country]),
        # country_pbook
        row[h.prop_is_branded],
        row[h.prop_starrating],
        cmf_to_n[row[h.distance_band]],
        lmh_to_n[row[h.hist_price_band]],
        lmh_to_n[row[h.popularity_band]],
        row[h.cnt],
        #row[h.is_booking],
        row[h.user_id],
        row[h.srch_destination_id],
        row[h.date_time],
        row[h.site_name],
        row[h.user_location_region],
        row[h.user_location_city],
        row[h.user_location_latitude],
        row[h.user_location_longitude],
    ]
    out.writerow(row)
