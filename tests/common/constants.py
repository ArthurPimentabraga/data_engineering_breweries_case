import pyspark.sql.types as sparkTypes

SOURCE_DATA = [
    {
        "id": "11111111-1111-1111-1111-111111111111",
        "name": "Brewery 1",
        "brewery_type": "micro",
        "address_1": "Address 1",
        "city": "City 1",
        "state_province": "State province 1",
        "postal_code": "11111-1111",
        "country": "Country 1",
        "longitude": -11.11111111,
        "latitude": 11.11111111,
        "phone": "1111111111",
        "state": "State 1",
        "street": "Street 1"
    }
]

MOCK_DATA = [
    {
        "id": "11111111-1111-1111-1111-111111111111",
        "name": "Brewery 1",
        "brewery_type": "micro",
        "address_1": "Address 1",
        "city": "City 1",
        "state_province": "State province 1",
        "postal_code": "11111-1111",
        "country": "Country 1",
        "longitude": -11.11111111,
        "latitude": 11.11111111,
        "phone": "1111111111",
        "state": "State 1",
        "street": "Street 1",
        "country_partition": "country_1"
    },
    {
        "id": "22222222-2222-2222-2222-222222222222",
        "name": "Brewery 2",
        "brewery_type": "micro",
        "address_1": "Address 2",
        "city": "City 2",
        "state_province": "State province 2",
        "postal_code": "11111-1111",
        "country": "Country 1",
        "longitude": -22.22222222,
        "latitude": 22.22222222,
        "phone": "2222222222",
        "state": "State 2",
        "street": "Street 2",
        "country_partition": "country_1"
    },
    {
        "id": "33333333-3333-3333-3333-333333333333",
        "name": "Brewery 3",
        "brewery_type": "large",
        "address_1": "Address 3",
        "city": "City 3",
        "state_province": "State province 3",
        "postal_code": "11111-1111",
        "country": "Country 1",
        "longitude": -33.33333333,
        "latitude": 33.33333333,
        "phone": "3333333333",
        "state": "State 3",
        "street": "Street 3",
        "country_partition": "country_1"
    }
]

FULL_SCHEMA = sparkTypes.StructType([
    sparkTypes.StructField('address_1', sparkTypes.StringType(), True), 
    sparkTypes.StructField('brewery_type', sparkTypes.StringType(), True), 
    sparkTypes.StructField('city', sparkTypes.StringType(), True), 
    sparkTypes.StructField('country', sparkTypes.StringType(), True), 
    sparkTypes.StructField('id', sparkTypes.StringType(), True), 
    sparkTypes.StructField('latitude', sparkTypes.DoubleType(), True), 
    sparkTypes.StructField('longitude', sparkTypes.DoubleType(), True), 
    sparkTypes.StructField('name', sparkTypes.StringType(), True), 
    sparkTypes.StructField('phone', sparkTypes.StringType(), True), 
    sparkTypes.StructField('postal_code', sparkTypes.StringType(), True), 
    sparkTypes.StructField('state', sparkTypes.StringType(), True), 
    sparkTypes.StructField('state_province', sparkTypes.StringType(), True), 
    sparkTypes.StructField('street', sparkTypes.StringType(), True), 
    sparkTypes.StructField('country_partition', sparkTypes.StringType(), True)
])

GOLD_SCHEMA = sparkTypes.StructType([
    sparkTypes.StructField('brewery_type', sparkTypes.StringType(), True), 
    sparkTypes.StructField('country', sparkTypes.StringType(), True), 
    sparkTypes.StructField('quantity_breweries', sparkTypes.LongType(), True), 
    sparkTypes.StructField('country_partition', sparkTypes.StringType(), True)
])