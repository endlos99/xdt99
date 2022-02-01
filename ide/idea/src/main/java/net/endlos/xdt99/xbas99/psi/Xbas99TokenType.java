package net.endlos.xdt99.xbas99.psi;

import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99.Xbas99Language;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class Xbas99TokenType extends IElementType {
    public Xbas99TokenType(@NotNull @NonNls String debugName) {
        super(debugName, Xbas99Language.INSTANCE);
    }

    @Override
    public String toString() {
        return "Xbas99TokenType." + super.toString();
    }
}
