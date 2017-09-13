package net.endlos.xdt99.xga99;

import com.intellij.navigation.ChooseByNameContributor;
import com.intellij.navigation.NavigationItem;
import com.intellij.openapi.project.Project;
import net.endlos.xdt99.xga99.Xga99Util;
import net.endlos.xdt99.xga99.psi.Xga99Labeldef;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

public class Xga99ChooseByNameContributor implements ChooseByNameContributor {
    @NotNull
    @Override
    public String[] getNames(Project project, boolean includeNonProjectItems) {
        List<Xga99Labeldef> labels = Xga99Util.findLabels(project);
        List<String> names = new ArrayList<String>(labels.size());
        for (Xga99Labeldef label : labels) {
            if (label.getName() != null && label.getName().length() > 0) {
                names.add(label.getName());
            }
        }
        return names.toArray(new String[names.size()]);
    }

    @NotNull
    @Override
    public NavigationItem[] getItemsByName(String name, String pattern, Project project, boolean includeNonProjectItems) {
        List<Xga99Labeldef> labels = Xga99Util.findLabels(project, null, name, 0, 0);
        return labels.toArray(new NavigationItem[labels.size()]);
    }
}
