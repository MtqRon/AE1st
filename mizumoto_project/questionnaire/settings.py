# スプレッドシートの列ラベル
SEX_LABEL        = "sex"
AGE_LABEL        = "age"
PREFECTURE_LABEL = "region"


# 性別のラベル
SEX_CATEGORIES = {
    "男性": "Male",
    "女性": "Female",
    "どちらでもない": "Other",
    "回答しない/その他": "No answer"
}

# 年齢区分のラベル
AGE_CATEGORIES = {
    "Under 19": "19歳以下",
    "20-29": "20-29歳",
    "30-39": "30-39歳",
    "40-49": "40-49歳",
    "50-59": "50-59歳",
    "60-69": "60-69歳",
    "Over 70": "70歳以上"
}

# 都道府県のラベル
PREFECTURE_CATEGORIES = {
    "北海道": "Hokkaido",
    "青森県": "Aomori",
    "岩手県": "Iwate",
    "宮城県": "Miyagi",
    "秋田県": "Akita",
    "山形県": "Yamagata",
    "福島県": "Fukushima",
    "茨城県": "Ibaraki",
    "栃木県": "Tochigi",
    "群馬県": "Gunma",
    "埼玉県": "Saitama",
    "千葉県": "Chiba",
    "東京都": "Tokyo",
    "神奈川県": "Kanagawa",
    "新潟県": "Niigata",
    "富山県": "Toyama",
    "石川県": "Ishikawa",
    "福井県": "Fukui",
    "山梨県": "Yamanashi",
    "長野県": "Nagano",
    "岐阜県": "Gifu",
    "静岡県": "Shizuoka",
    "愛知県": "Aichi",
    "三重県": "Mie",
    "滋賀県": "Shiga",
    "京都府": "Kyoto",
    "大阪府": "Osaka",
    "兵庫県": "Hyogo",
    "奈良県": "Nara",
    "和歌山県": "Wakayama",
    "鳥取県": "Tottori",
    "島根県": "Shimane",
    "岡山県": "Okayama",
    "広島県": "Hiroshima",
    "山口県": "Yamaguchi",
    "徳島県": "Tokushima",
    "香川県": "Kagawa",
    "愛媛県": "Ehime",
    "高知県": "Kochi",
    "福岡県": "Fukuoka",
    "佐賀県": "Saga",
    "長崎県": "Nagasaki",
    "熊本県": "Kumamoto",
    "大分県": "Oita",
    "宮崎県": "Miyazaki",
    "鹿児島県": "Kagoshima",
    "沖縄県": "Okinawa"
}

# 都道府県の座標データ
PREFECTURE_COORDINATES = {
    "Hokkaido": {"lat": 43.064359, "lon": 141.346814},
    "Aomori": {"lat": 40.822308, "lon": 140.740354},
    "Iwate": {"lat": 39.703619, "lon": 141.152684},
    "Miyagi": {"lat": 38.268839, "lon": 140.872103},
    "Akita": {"lat": 39.718600, "lon": 140.102401},
    "Yamagata": {"lat": 38.240437, "lon": 140.363314},
    "Fukushima": {"lat": 37.760799, "lon": 140.474709},
    "Ibaraki": {"lat": 36.341813, "lon": 140.446793},
    "Tochigi": {"lat": 36.565725, "lon": 139.883565},
    "Gunma": {"lat": 36.391208, "lon": 139.060156},
    "Saitama": {"lat": 35.857428, "lon": 139.648933},
    "Chiba": {"lat": 35.607266, "lon": 140.106292},
    "Tokyo": {"lat": 35.689521, "lon": 139.691704},
    "Kanagawa": {"lat": 35.447753, "lon": 139.642514},
    "Niigata": {"lat": 37.902418, "lon": 139.023221},
    "Toyama": {"lat": 36.695290, "lon": 137.211338},
    "Ishikawa": {"lat": 36.594682, "lon": 136.625573},
    "Fukui": {"lat": 36.065219, "lon": 136.221642},
    "Yamanashi": {"lat": 35.664158, "lon": 138.568449},
    "Nagano": {"lat": 36.651289, "lon": 138.181224},
    "Gifu": {"lat": 35.391227, "lon": 136.722291},
    "Shizuoka": {"lat": 34.976978, "lon": 138.383054},
    "Aichi": {"lat": 35.181467, "lon": 136.906565},
    "Mie": {"lat": 34.730283, "lon": 136.508591},
    "Shiga": {"lat": 35.004531, "lon": 135.868590},
    "Kyoto": {"lat": 35.011564, "lon": 135.768149},
    "Osaka": {"lat": 34.686316, "lon": 135.526237},
    "Hyogo": {"lat": 34.691279, "lon": 135.183025},
    "Nara": {"lat": 34.685333, "lon": 135.804754},
    "Wakayama": {"lat": 34.226034, "lon": 135.167506},
    "Tottori": {"lat": 35.503869, "lon": 134.237672},
    "Shimane": {"lat": 35.472297, "lon": 133.050499},
    "Okayama": {"lat": 34.661751, "lon": 133.935359},
    "Hiroshima": {"lat": 34.385289, "lon": 132.455292},
    "Yamaguchi": {"lat": 34.186121, "lon": 131.470500},
    "Tokushima": {"lat": 34.340149, "lon": 134.043444},
    "Kagawa": {"lat": 34.340149, "lon": 134.043444},
    "Ehime": {"lat": 33.839160, "lon": 132.765575},
    "Kochi": {"lat": 33.559705, "lon": 133.531080},
    "Fukuoka": {"lat": 33.590184, "lon": 130.401689},
    "Saga": {"lat": 33.249367, "lon": 130.298822},
    "Nagasaki": {"lat": 32.750286, "lon": 129.877667},
    "Kumamoto": {"lat": 32.789828, "lon": 130.741667},
    "Oita": {"lat": 33.238194, "lon": 131.608609},
    "Miyazaki": {"lat": 31.911090, "lon": 131.423855},
    "Kagoshima": {"lat": 31.560148, "lon": 130.558157},
    "Okinawa": {"lat": 26.212401, "lon": 127.680932}
} 