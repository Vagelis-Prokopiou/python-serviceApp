#include <iostream>

using namespace std;

int validate_date(user_date, today) {
//    Checks diff of provided date in comparison to today.
    year, month, day = user_date.strip().split('-');
    date = datetime.date(int(year), int(month), int(day));
    if (today > date) && (today - date) > datetime.timedelta(days = 547)
    {
        return -1;

    }
    return 0;
}

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}