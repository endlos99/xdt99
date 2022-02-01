package net.endlos.xdt99.xas99r;

import com.intellij.navigation.ChooseByNameContributor;
import com.intellij.navigation.NavigationItem;
import com.intellij.openapi.project.Project;
import net.endlos.xdt99.xas99r.psi.Xas99RLabeldef;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

public class Xas99RChooseByNameContributor implements ChooseByNameContributor {

    @Override
    public String @NotNull [] getNames(Project project, boolean includeNonProjectItems) {
        List<Xas99RLabeldef> labels = Xas99RUtil.findLabels(project);
        List<String> names = new ArrayList<String>(labels.size());
        for (Xas99RLabeldef label : labels) {
            if (label.getName() != null && label.getName().length() > 0) {
                names.add(label.getName());
            }
        }
        return names.toArray(new String[names.size()]);
    }

    @Override
    public NavigationItem @NotNull [] getItemsByName(String name, String pattern, Project project, boolean includeNonProjectItems) {
        List<Xas99RLabeldef> labels = Xas99RUtil.findLabels(project, name, 0, null, 0, false);
        return labels.toArray(new NavigationItem[labels.size()]);
    }

}
