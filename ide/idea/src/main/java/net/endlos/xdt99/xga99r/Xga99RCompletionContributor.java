package net.endlos.xdt99.xga99r;

import com.intellij.codeInsight.completion.*;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.patterns.PlatformPatterns;
import com.intellij.psi.PsiElement;
import com.intellij.util.ProcessingContext;
import net.endlos.xdt99.xga99r.psi.Xga99RFile;
import net.endlos.xdt99.xga99r.psi.Xga99RLabeldef;
import net.endlos.xdt99.xga99r.psi.Xga99ROpLabel;
import net.endlos.xdt99.xga99r.psi.Xga99RTypes;
import org.jetbrains.annotations.NotNull;

import java.util.List;

public class Xga99RCompletionContributor extends CompletionContributor {
    private final String dummy = CompletionUtilCore.DUMMY_IDENTIFIER_TRIMMED.toUpperCase();

    public Xga99RCompletionContributor() {
        extend(CompletionType.BASIC, PlatformPatterns.psiElement(Xga99RTypes.IDENT),
                new CompletionProvider<CompletionParameters>() {
                    @Override
                    protected void addCompletions(@NotNull CompletionParameters parameters,
                                                  @NotNull ProcessingContext context,
                                                  @NotNull CompletionResultSet resultSet) {
                        PsiElement parent = parameters.getPosition().getParent();
                        if (parent instanceof Xga99ROpLabel ||
                                (parent instanceof Xga99RFile &&
                                        parameters.getPosition().getPrevSibling().getNode().getElementType() == Xga99RTypes.OP_AT)) {
                            getCompletions(parameters.getPosition(), resultSet);
                        }
                    }
                }
        );
    }

    private void getCompletions(@NotNull PsiElement element, @NotNull CompletionResultSet resultSet) {
        Project project = element.getProject();
        String label = element.getText().toUpperCase();
        if (label.endsWith(dummy)) {
            label = label.substring(0, label.length() - dummy.length());
        }
        List<Xga99RLabeldef> labeldefs = Xga99RUtil.findLabels(project, label, 0, element, 0, true);
        for (final Xga99RLabeldef labeldef : labeldefs) {
            if (labeldef.getName() != null && labeldef.getName().length() > 0) {
                resultSet.addElement(LookupElementBuilder.create(labeldef).
                        withIcon(Xga99RIcons.FILE).
                        withTypeText(labeldef.getContainingFile().getName())
                );
            }
        }
    }

}
