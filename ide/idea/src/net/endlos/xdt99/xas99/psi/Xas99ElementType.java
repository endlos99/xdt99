package net.endlos.xdt99.xas99.psi;

import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xas99.Xas99Language;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class Xas99ElementType extends IElementType {
    public Xas99ElementType(@NotNull @NonNls String debugName) {
        super(debugName, Xas99Language.INSTANCE);
    }
}
