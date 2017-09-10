import csv
import IPython
import numpy as np
# IPython.terminal.embed.embed()
import pandas as pd
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from keras.utils import to_categorical

do_train = False

col_types = {
    "click_weekday": float,
    "click_hour": float,
    "ln_country_popularity": float,
    "orig_destination_distance": float,
    "is_mobile": float,
    "is_package": float,
    "chan_231": float,
    "chan_262": float,
    "chan_293": float,
    "chan_324": float,
    "chan_355": float,
    "chan_386": float,
    "chan_417": float,
    "chan_448": float,
    "chan_479": float,
    "chan_510": float,
    "chan_541": float,
    "days_to_booking": float,
    "duration_of_stay": float,
    "srch_adults_cnt": float,
    "srch_children_cnt": float,
    "srch_rm_cnt": float,
    "same_country": float,
    "prop_is_branded": float,
    "prop_starrating": float,
    "distance_band_n": float,
    "hist_price_band_n": int,
    "popularity_band_n": float,
    "cnt": float,
    #"is_booking": int,
    "user_id": str,
    "srch_destination_id": str,
    "date_time": str,
    "site_name": str,
    "user_location_region": str,
    "user_location_city": str,
    "user_location_latitude": float,
    "user_location_longitude": float,
}

data = pd.read_csv("train.txt", sep='\t', dtype=col_types, index_col=None)
dest = pd.read_csv("dest.txt", sep='\t', index_col=None)

#IPython.terminal.embed.embed()

X = data[[
    "click_weekday",
    "click_hour",
    "ln_country_popularity",
    "orig_destination_distance",
    "is_mobile",
    "is_package",
    #"chan_231",
    #"chan_262",
    #"chan_293",
    #"chan_324",
    #"chan_355",
    #"chan_386",
    #"chan_417",
    #"chan_448",
    #"chan_479",
    #"chan_510",
    #"chan_541",
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
]]

#IPython.terminal.embed.embed()

Y = to_categorical(data[
    "hist_price_band_n"
    #"is_booking"
])


#IPython.terminal.embed.embed()

X = X.values

d_in = X.shape[1]
d_out = 5

m = Sequential()
m.add(Dense(20, input_shape=(d_in,), activation='relu'))
# m.add(Dropout(0.2))
m.add(Dense(20,  activation='relu'))
m.add(Dense(20,  activation='relu'))
# m.add(Dropout(0.2))
m.add(Dense(d_out, activation='softmax'))
m.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

pred = None

if do_train:
    m.fit(X, Y, validation_split=0.2, batch_size=1024, epochs=50, verbose=1)
    m.save_weights("weights")
    pred = m.predict_proba(X)
    with open("predictions.txt", "w", newline='') as out:
        wr = csv.writer(out, delimiter='\t')
        for row in pred:
            wr.writerow(row)
else:
    m.load_weights("weights")
    pred = pd.read_csv("predictions.txt", sep='\t', dtype=float, header=None).values

show_cols = [
    #"click_weekday",
    #"click_hour",
    #"ln_country_popularity",
    "orig_destination_distance",
    "is_mobile",
    "is_package",
    #"chan_231",
    #"chan_262",
    #"chan_293",
    #"chan_324",
    #"chan_355",
    #"chan_386",
    #"chan_417",
    #"chan_448",
    #"chan_479",
    #"chan_510",
    #"chan_541",
    "days_to_booking",
    "duration_of_stay",
    "srch_adults_cnt",
    "srch_children_cnt",
    "srch_rm_cnt",
    #"same_country",
    "prop_is_branded",
    "prop_starrating",
    "distance_band_n",
    "hist_price_band_n",
    "popularity_band_n",
    #"cnt",
    #"user_id",
    #"srch_destination_id",
    #"date_time",
    #"site_name",
    #"user_location_region",
    #"user_location_city",
    #"user_location_latitude",
    #"user_location_longitude",
]

save_cols = [
    "click_weekday",
    "click_hour",
    "ln_country_popularity",
    "orig_destination_distance",
    "is_mobile",
    "is_package",
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
    "user_id",
    "srch_destination_id",
    "date_time",
    "site_name",
    "user_location_region",
    "user_location_city",
    "user_location_latitude",
    "user_location_longitude",
]

for_tab = open('tableau.txt', 'w')
wr = csv.writer(for_tab, delimiter='\t')

wr.writerow(save_cols)

#IPython.terminal.embed.embed()

dest_v = dest.values

for i in range(len(X)):
    p = pred[i]
    if not (pred[i][0] >= 0.9 and Y[i][0] == 0.0 or
            pred[i][1] >= 0.9 and Y[i][0] == 0.0 and Y[i][1] == 0.0 or
            pred[i][2] >= 0.9 and Y[i][0] == 0.0 and Y[i][1] == 0.0 and Y[i][2] == 0.0 or
            pred[i][3] >= 0.9 and Y[i][0] == 0.0 and Y[i][1] == 0.0 and Y[i][2] == 0.0 and Y[i][3] == 0.0):
        continue
    print("Prediction:", pred[i])
    print("Actual:", Y[i])
    for column in show_cols:
        print("  {}: {}".format(column, data[column][i]))
    dest_id = int(data['srch_destination_id'][i])
    for v in dest_v:
        if v[0] == dest_id:
            print(v[1])
            print("location:", v[2], v[3])
    print()

#for p in range(5):
#    tmp = sorted([x for x in range(len(pred))], key=lambda i: pred[i][p], reverse=True)
#    #IPython.terminal.embed.embed()
#    print("Price " + "$"*(p+1))
#    for i in range(10):
#        #IPython.terminal.embed.embed()
#        wr.writerow(data[save_cols].values[tmp[i]])

IPython.terminal.embed.embed()

