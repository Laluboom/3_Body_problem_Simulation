
public class Position_Vector_Subtraction {
    private double x;
    private double y;
    private double z;

    public Position_Vector_Subtraction(double x, double y, double z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public static Position_Vector_Subtraction subtract(Position_Vector_Subtraction a, Position_Vector_Subtraction b) {
        double newX = a.getX() - b.getX();
        double newY = a.getY() - b.getY();
        double newZ = a.getZ() - b.getZ();
        return new Position_Vector_Subtraction(newX, newY, newZ);
    }

    public double getX() {
        return x;
    }

    public void setX(double x) {
        this.x = x;
    }

    public double getY() {
        return y;
    }

    public void setY(double y) {
        this.y = y;
    }

    public double getZ() {
        return z;
    }

    public void setZ(double z) {
        this.z = z;
    }

    public static void main(String[] args) {
        Position_Vector_Subtraction a = new Position_Vector_Subtraction(5, 3, 5);
        Position_Vector_Subtraction b = new Position_Vector_Subtraction(1, 1, 1);
        Position_Vector_Subtraction result = Position_Vector_Subtraction.subtract(a, b);
        System.out.println("Result: (" + result.getX() + ", " + result.getY() + ", " + result.getZ() + ")");
    }
}