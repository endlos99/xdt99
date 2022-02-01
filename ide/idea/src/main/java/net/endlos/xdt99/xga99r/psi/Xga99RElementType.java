package net.endlos.xdt99.xga99r.psi;

import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xga99r.Xga99RLanguage;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class Xga99RElementType extends IElementType {
    public Xga99RElementType(@NotNull @NonNls String debugName) {
        super(debugName, Xga99RLanguage.INSTANCE);
    }
}
