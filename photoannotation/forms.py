from flask_wtf import FlaskForm
from wtforms import StringField, FileField, DateField, SelectField, SubmitField


class UploadForm(FlaskForm):
    username = StringField("username")
    photo = FileField("Choose file")
    name = StringField("Photo name")
    type = StringField("Photo type")
    date = DateField('Date')
    height = StringField('Height')
    width = StringField('Width')
    size = StringField('Size')
    corporation = StringField('Device maker')
    model = StringField('Device model')
    exposureTime = StringField('Exposure time')
    exposureProgram = StringField('Exposure program')
    focal = StringField('Focal length')
    flash = StringField('Flash mode')
    event = StringField('Event name')
    location = StringField('Location')
    album = SelectField('Album', choices=[('0', '-----'), ('1', 'Birthday'), ('2', 'Eid')])
    weather = StringField('Weather')
    group = SelectField('Group', choices=[('0', '----'), ('1', 'Friends'), ('2', 'Family')])
    people = StringField('People')
    tag = StringField('Tag')
    upload = SubmitField('Upload')


class AlbumForm(UploadForm):
    upload = SubmitField('Update')


class SearchForm(AlbumForm):
    searchTime = SelectField('Timestamp', choices=[('0', '----'), ('1', 'Morning'), ('2', 'Noon')])
    searchEvent = StringField('Event')
    searchLocation = StringField('Location')
    searchWeather = SelectField('Weather', choices=[('0', '----'), ('1', 'Rainy'), ('2', 'Cloudy')])
    searchGroup = SelectField('Group', choices=[('0', '----'), ('1', 'Friend'), ('2', 'Family')])
    searchAlbum = SelectField('Album', choices=[('0', '----'), ('1', 'Birthday'), ('2', 'Eid')])
    searchDate = DateField('Date')
    searchTag = StringField('Tag')

