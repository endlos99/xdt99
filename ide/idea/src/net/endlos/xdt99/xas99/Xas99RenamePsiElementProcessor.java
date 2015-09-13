package net.endlos.xdt99.xas99;

import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiElement;
import com.intellij.refactoring.rename.RenamePsiElementProcessor;
import com.intellij.refactoring.rename.UnresolvableCollisionUsageInfo;
import com.intellij.usageView.UsageInfo;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import net.endlos.xdt99.xas99.psi.Xas99OpLabel;
import org.jetbrains.annotations.NotNull;

import java.util.List;
import java.util.Map;

import static net.endlos.xdt99.xas99.Xas99Util.findLabels;

public class Xas99RenamePsiElementProcessor extends RenamePsiElementProcessor {

    public boolean canProcessElement(@NotNull final PsiElement element) {
        return element instanceof Xas99OpLabel || element instanceof Xas99Labeldef;
    }

    @Override
    public void findCollisions(PsiElement element,
                               final String newName,
                               Map<? extends PsiElement, String> allRenames,
                               List<UsageInfo> result) {
        Project project = element.getProject();
        for (final Map.Entry<? extends PsiElement, String> e: allRenames.entrySet()) {
            PsiElement label = e.getKey();
            String newtext = e.getValue().toUpperCase();
            List<Xas99Labeldef> others = findLabels(project, null, newtext, 0, 0);
            for (Xas99Labeldef other : others) {
                result.add(new UnresolvableCollisionUsageInfo(other, label) {
                    @Override
                    public String getDescription() {
                        return "Duplicate symbols: " + e.getValue();
                    }
                });
            }
        }
    }
}
