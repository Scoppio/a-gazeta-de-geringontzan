from django.contrib import admin
from .exportcsv import runDoraR_action, export_as_csv_action, runTestAPI_action
from .models import apikeys, archive


# Register your models here
class apikeysModelAdmin(admin.ModelAdmin):

    actions = [
            export_as_csv_action("CSV Export"),
            runDoraR_action("Run Dora R."),
            runTestAPI_action("test if api"),
        ]
    list_display = ["username","email", "server", "subscribe", "validToken"]
    list_filter = ["server", "subscribe", "validToken"]
    saerch_fields = ["email", "username"]
    class Meta:
        model = apikeys

class archiveModelAdmin(admin.ModelAdmin):
    actions = [
            export_as_csv_action("CSV Export"),
            runDoraR_action("Run Dora R."),
        ]
    list_display = ["matchid", "date","hero", "hero_deck",
                    "opponent_hero", "opponent_deck", "result"]
    list_filter = ["date", "hero", "hero_deck",
                    "opponent_hero", "opponent_deck"]
    search_fields = ["cards", "opponent_cards"]

    class Meta:
        model = archive

admin.site.register(apikeys, apikeysModelAdmin)
admin.site.register(archive, archiveModelAdmin)
