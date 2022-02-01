package net.endlos.xdt99.xbas99l.psi;

import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99l.Xbas99LLanguage;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class Xbas99LTokenType extends IElementType {
    public Xbas99LTokenType(@NotNull @NonNls String debugName) {
        super(debugName, Xbas99LLanguage.INSTANCE);
    }

    @Override
    public String toString() {
        return "Xbas99LTokenType." + super.toString();
    }
}
