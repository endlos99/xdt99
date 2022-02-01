package net.endlos.xdt99.xas99;

import com.intellij.lang.documentation.AbstractDocumentationProvider;
import com.intellij.lang.documentation.DocumentationMarkup;
import com.intellij.psi.PsiElement;
import com.intellij.psi.presentation.java.SymbolPresentationUtil;
import net.endlos.xdt99.common.IntWrapper;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xas99DocumentationProvider extends AbstractDocumentationProvider {

    @Override
    public @Nullable String generateHoverDoc(@NotNull PsiElement element, @Nullable PsiElement originalElement) {
        return generateDoc(element, originalElement);
    }

    @Override
    // show line of label definition when hovering/asking for label use
    public @Nullable String generateDoc(PsiElement element, @Nullable PsiElement originalElement) {
        if (element instanceof Xas99Labeldef) {  // for some reason, we get Labeldef instead of OpLabel
            final String symbol = ((Xas99Labeldef) element).getName();
            IntWrapper lino = new IntWrapper(0);
            final String def = Xas99Util.getLabeldefText((Xas99Labeldef) element, lino);  // modified lino
            if (def == null)
                return null;
            final String filename = SymbolPresentationUtil.getFilePathPresentation(element.getContainingFile());
            return renderFullDoc(symbol, def, filename, lino);
        }
        return null;
    }

    // show hint
    private String renderFullDoc(String symbol, String def, String filename, IntWrapper lino) {
        StringBuilder sb = new StringBuilder();
        sb.append(DocumentationMarkup.DEFINITION_START);
        sb.append(def);
        sb.append(DocumentationMarkup.DEFINITION_END);
        sb.append(DocumentationMarkup.CONTENT_START);
        addKeyValueSection("File:", filename, sb);
        addKeyValueSection("Line number:", Integer.toString(lino.get()), sb);
        sb.append(DocumentationMarkup.CONTENT_END);
        return sb.toString();
    }

    private void addKeyValueSection(String key, String value, StringBuilder sb) {
        sb.append(DocumentationMarkup.SECTION_HEADER_START);
        sb.append(key);
        sb.append(DocumentationMarkup.SECTION_SEPARATOR);
        sb.append(value);
        sb.append(DocumentationMarkup.SECTION_END);
    }

}
