package net.endlos.xdt99.xga99.psi;

import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xga99.Xga99Language;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class Xga99ElementType extends IElementType {
    public Xga99ElementType(@NotNull @NonNls String debugName) {
        super(debugName, Xga99Language.INSTANCE);
    }
}
