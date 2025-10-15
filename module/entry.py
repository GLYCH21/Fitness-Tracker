
class Entry:
    def __init__(self, user_info: dict, activity: str, details: dict, duration=None, reps=None, sets=None):
        self.user_info = user_info
        self.activity = activity
        self.met = details.get("MET", 1)
        self.is_valid = False
        self.details = details

        from resource import common
        if details.get("type") == "time":
            self.duration = common.validate_number(duration)
            self.is_valid = self.duration > 0
        else:
            self.reps = common.validate_number(reps)
            self.sets = common.validate_number(sets) or 1
            self.is_valid = self.reps > 0

    @property
    def formatted_details(self) -> str:
        if hasattr(self, "duration"):
            return f"{self.duration} min{'s' if self.duration != 1 else ''}"
        else:
            return f"{self.reps} rep{'s' if self.reps > 1 else ''}, {self.sets} set{'s' if self.sets > 1 else ''}"

    @property
    def calories_burned(self) -> float:
        if hasattr(self, "duration"):
            print(self.user_info)
            return round(self.met * self.user_info["weight"] * (self.duration/60), 2)
        else:
            time_per_rep_sec = 1
            rest_time_per_set_sec = 60
            # Calculate the total active time (time spent performing reps)
            total_active_time_sec = self.reps * self.sets * time_per_rep_sec

            # Calculate the total rest time (rest between sets)
            total_rest_time_sec = (self.sets - 1) * rest_time_per_set_sec  # No rest after the last set

            # Total time in seconds (active + rest)
            total_time_sec = total_active_time_sec + total_rest_time_sec

            # Convert total time to hours
            total_time_hours = total_time_sec / 3600

            # Calculate calories burned using the MET formula
            calories_burned = self.details["MET"] * self.user_info["weight"] * total_time_hours
            return round(calories_burned, 2)

    @property
    def entry_submission(self) -> list:
        return [self.activity, self.formatted_details, self.calories_burned]