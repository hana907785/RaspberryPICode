#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>// 유닉스에서 사용하는 C 컴파일러 헤더파일



using namespace std;

#define GPIO  "/sys/class/gpio/"
#define FLASH_DELAY 1000000

class LED {
private:
	string gpioPath;
	int gpioNumber;
	void writeSysfs(string path, string filename, string value);

public:
	LED(int gpioNumber);
	virtual void turnOn();
	virtual void turnOff();
	virtual void displayState();
	virtual ~LED();
};

LED::LED(int gpioNumber) {
	this->gpioNumber = gpioNumber;
	gpioPath = string(GPIO "gpio") + to_string(gpioNumber) + string("/");
	writeSysfs(string(GPIO), "export", to_string(gpioNumber));
	usleep(100000);
	writeSysfs(gpioPath, "direction", "out");
}
void LED::writeSysfs(string path, string filename, string value) {
	ofstream fs;
	fs.open((path + filename).c_str());
	fs << value;
	fs.close();
}

void LED::turnOn() {
	writeSysfs(gpioPath, "value", "1");
}

void LED::turnOff() {
	writeSysfs(gpioPath, "value", "0");
}
void LED::displayState() {
	ifstream fs;
	fs.open((gpioPath + "value").c_str());
	string line;
	cout << "The current LED state is ";
	while (getline(fs, line)) cout << line << endl;
	fs.close();
}
LED::~LED() {
	cout << "Destroying the LED with GPIO number " << gpioNumber << endl;
	writeSysfs(string(GPIO), "unexport", to_string(gpioNumber));
}

int main(int argc, char* argv[]) {

	cout << "Starting the 3Week HW1 program" << endl;

	LED ledRed(27), ledGreen(22), ledYellow(23);

	for (int i = 0; i < 20; i++) {
		ledRed.turnOn();
		ledGreen.turnOff();
		ledYellow.turnOff();
		usleep(FLASH_DELAY);

		ledRed.turnOff();
		ledGreen.turnOn();
		ledYellow.turnOff();
		usleep(FLASH_DELAY);

		ledRed.turnOff();
		ledGreen.turnOff();
		ledYellow.turnOn();
		usleep(FLASH_DELAY);

		ledRed.turnOff();
		ledGreen.turnOn();
		ledYellow.turnOff();
		usleep(FLASH_DELAY);

	}
	ledRed.turnOff();
	ledGreen.turnOff();
	ledYellow.turnOff();

	ledRed.displayState();
	ledGreen.displayState();
	ledYellow.displayState();
	cout << "Finished the makeLEDs program" << endl;

	return 0;

}
