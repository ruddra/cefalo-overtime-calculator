import csv
import datetime
import operator

CSV_FILE = './overtime.csv'
CSV_SEP = ","
DATETIME_FORMAT = "%m/%d/%Y %H:%M"
WORKING_HOURS = 9
DATE_ROW = 0
ENTRY_ROW = 1
EXIT_ROW = 2


class CalculateOverTime(object):
    def __init__(self):
        self.csv_file = CSV_FILE
        self.dt_format = DATETIME_FORMAT
        self.working_hours = WORKING_HOURS
        self.date_row = DATE_ROW
        self.entry_row = ENTRY_ROW
        self.exit_row = EXIT_ROW
        self.csv_sep = CSV_SEP
        self.weekly_overtime_dict = {}
        self.weekly_overtime = datetime.timedelta(0)
        self.current_week = -1
        self.total_overtime = datetime.timedelta(0)

    def get_minus_time(self, td):
         td = datetime.timedelta(days=1) - td
         sign = "-"
         return "{}{}:{}".format(sign, (td.seconds) // 3600, td.seconds // 60 % 60)

    def get_plus_time(self, td):
         sign = "+"
         return "{}{}:{}".format(sign, (td.days*86400 + td.seconds) // 3600, td.seconds // 60 % 60)
        

    def get_hour_minutes(self, td, return_type="str"):
        if return_type == "str":
            sign = "+"
            if td.days <= -1:
                return self.get_minus_time(td)
            else:
                return self.get_plus_time(td)
        else:
            return (td.days*86400 + td.seconds)//3600, (td.seconds//60)%60        

    def get_overtime(self, start_time, end_time):
        current_time =  end_time - start_time
        hour, minute = self.get_hour_minutes(current_time, return_type="int")
        overtime = current_time - datetime.timedelta(hours=WORKING_HOURS)
        return overtime

    def generate_daily_report(self, date, start, end, overtime):
        overtime = self.get_hour_minutes(overtime)
        print("Date: {date: <10}, Start: {start: <5}, End: {end: <5},"
        " Overtime: {overtime: <6}".format(
            date = date,
            start = start, 
            end = end, 
            overtime = overtime
        ))

    def get_datetime(self, date, time):
        time = time.replace(" ", "")
        return datetime.datetime.strptime('{} {}'.format(
                date,
                time
            ), DATETIME_FORMAT
        )

    def store_week_report(self, report):
        self.weekly_overtime_list.append(report)        

    def get_week(self, datetime_obj):
        return datetime_obj.strftime("%V")

    def update_weekly_overtime(self, overtime):
        self.weekly_overtime += overtime

    def get_weekly_report(self, week_no):
        return self.weekly_overtime_dict.get(week_no, datetime.timedelta(0))

    def create_weekly_report(self, overtime):
        return { 'overtime' : overtime }

    def get_updated_overtime(self, week_overtime, overtime):
        return week_overtime + overtime

    def update_weekly_report(self, week_no, overtime):
        weekly_overtime = self.get_weekly_report(week_no)
        updated_overtime =  self.get_updated_overtime(weekly_overtime, overtime)
        self.weekly_overtime_dict[week_no] = updated_overtime

    def update_total_overtime(self, curr_overtime):
        self.total_overtime += curr_overtime

    def process_csv(self):
        try:
            self.show_header("Daily Overtime", 61)
            with open(self.csv_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=self.csv_sep)
                line = 0
                for row in csv_reader:
                    line += 1
                    if line == 1:
                        continue
                    date = row[self.date_row]
                    entry = row[self.entry_row]
                    end = row[self.exit_row]
                    entry_time = self.get_datetime(date, entry)
                    exit_time = self.get_datetime(date, end)
                    current_week = self.get_week(entry_time)
                    if entry_time == exit_time:
                        continue
                    current_overtime = self.get_overtime(entry_time, exit_time) 
                    self.update_total_overtime(current_overtime)
                    self.update_weekly_report(current_week, current_overtime)
                    self.generate_daily_report(date, entry, end, current_overtime)
            print('-'*61)
        except IOError:
            print("File not found at {}".format(self.csv_file))

        except IndexError:
            print("Delimiter '{}' not found".format(self.csv_sep))
        
        except ValueError as e:
            print(str(e))
        
        except Exception as e:
            print("Generic Exception")
            print(str(e))
        
        
    def display_weekly_entry(self, week_no, overtime):
        overtime = self.get_hour_minutes(overtime)
        print(
            "Week {week_no: <3} "
            "Overtime: {overtime: <6}".format(
                week_no = week_no,
                overtime = overtime)
        )

    def show_header(self, text="", max_line=24):
        print('-'*max_line)
        print(text.center(max_line))
        print('-'*max_line)


    def generate_weekly_report(self):
        max_line = 24
        self.show_header("Weekly Report", max_line)
        total_overtime = datetime.timedelta(0)
        for key, value in sorted(self.weekly_overtime_dict.items(), key=operator.itemgetter(0)):
            self.display_weekly_entry(key, value)
            total_overtime += value
        print('-' * max_line)
        
    def show_total_overtime(self):
        hours, minutes = self.get_hour_minutes(self.total_overtime, return_type="int")
        self.show_header("Total Overtime", 22)
        print(
            "Hours: {hours: <3} Minutes: {minutes: <3}".format(
                hours = hours,
                minutes = minutes
            )
        )
        print('-'*22)

if __name__ == "__main__":
    overtime = CalculateOverTime()
    overtime.process_csv()
    overtime.generate_weekly_report()
    overtime.show_total_overtime()
    