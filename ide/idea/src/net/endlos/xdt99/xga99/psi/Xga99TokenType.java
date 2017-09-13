package net.endlos.xdt99.xga99.psi;

import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xga99.Xga99Language;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class Xga99TokenType extends IElementType {
    public Xga99TokenType(@NotNull @NonNls String debugName) {
        super(debugName, Xga99Language.INSTANCE);
    }

    @Override
    public String toString() {
        return "Xga99TokenType." + super.toString();
    }
}
