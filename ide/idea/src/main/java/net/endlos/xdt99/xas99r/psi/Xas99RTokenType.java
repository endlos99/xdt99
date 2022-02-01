package net.endlos.xdt99.xas99r.psi;

import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xas99r.Xas99RLanguage;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class Xas99RTokenType extends IElementType {
    public Xas99RTokenType(@NotNull @NonNls String debugName) {
        super(debugName, Xas99RLanguage.INSTANCE);
    }

    @Override
    public String toString() {
        return "Xas99RTokenType." + super.toString();
    }
}
