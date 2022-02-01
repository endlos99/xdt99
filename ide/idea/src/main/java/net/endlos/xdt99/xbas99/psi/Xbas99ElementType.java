package net.endlos.xdt99.xbas99.psi;

import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99.Xbas99Language;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class Xbas99ElementType extends IElementType {
    public Xbas99ElementType(@NotNull @NonNls String debugName) {
        super(debugName, Xbas99Language.INSTANCE);
    }
}
