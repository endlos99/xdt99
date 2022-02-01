package net.endlos.xdt99.common;

// wraps an integer for pass-by-value
public class IntWrapper {
    private int value;

    public IntWrapper(int value) {
        this.value = value;
    }

    public int get() {
        return value;
    }

    public void set(int value) {
        this.value = value;
    }

    public int inc() {
        return ++this.value;
    }

}
