package net.endlos.xdt99.xbas99l.psi;

import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99l.Xbas99LLanguage;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class Xbas99LElementType extends IElementType {
    public Xbas99LElementType(@NotNull @NonNls String debugName) {
        super(debugName, Xbas99LLanguage.INSTANCE);
    }
}
