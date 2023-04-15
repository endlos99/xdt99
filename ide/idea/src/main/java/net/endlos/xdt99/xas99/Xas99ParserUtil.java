package net.endlos.xdt99.xas99;

import com.intellij.lang.PsiBuilder;
import com.intellij.lang.parser.GeneratedParserUtilBase;
import net.endlos.xdt99.xas99.psi.Xas99Types;

import java.util.HashSet;
import java.util.Set;

import static net.endlos.xdt99.xas99.parser.Xas99Parser.*;


public class Xas99ParserUtil extends GeneratedParserUtilBase {
    static Set<String> knownAliases = new HashSet<>();

    public static boolean registerAlias(PsiBuilder builder, int level) {

        // Detect three different token sequences:
        // - label REQU
        // - label : REQU
        // - label : \n REQU
        if (builder.lookAhead(1) == Xas99Types.DIR_RA ||
                (builder.lookAhead(1) == Xas99Types.OP_COLON &&
                        (builder.lookAhead(2) == Xas99Types.DIR_RA ||
                                builder.lookAhead(3) == Xas99Types.DIR_RA))) {
            String name = builder.getTokenText().toUpperCase();
            knownAliases.add(name);
        }

        return false;
    }

    public static boolean parseMacroSymbol(PsiBuilder builder, int level) {
        boolean result;

        String name = builder.getTokenText().toUpperCase();
        if (knownAliases.contains(name)) {
            result = opRegister(builder, level + 1);
        } else {
            result = opLabel(builder, level + 1);
        }

        return result;
    }

}
