package net.endlos.xdt99.xga99r;

import com.intellij.navigation.ChooseByNameContributor;
import com.intellij.navigation.NavigationItem;
import com.intellij.openapi.project.Project;
import net.endlos.xdt99.xga99r.psi.Xga99RLabeldef;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

public class Xga99RChooseByNameContributor implements ChooseByNameContributor {

    @Override
    public String @NotNull [] getNames(Project project, boolean includeNonProjectItems) {
        List<Xga99RLabeldef> labels = Xga99RUtil.findLabels(project);
        List<String> names = new ArrayList<String>(labels.size());
        for (Xga99RLabeldef label : labels) {
            if (label.getName() != null && label.getName().length() > 0) {
                names.add(label.getName());
            }
        }
        return names.toArray(new String[names.size()]);
    }

    @Override
    public NavigationItem @NotNull [] getItemsByName(String name, String pattern, Project project, boolean includeNonProjectItems) {
        List<Xga99RLabeldef> labels = Xga99RUtil.findLabels(project, name, 0, null, 0, false);
        return labels.toArray(new NavigationItem[labels.size()]);
    }

}
