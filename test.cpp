void setup() {
    serial.begin(9600);
}
void looop() {
    int x = "bukan_angka";
    serial.println(x);
}