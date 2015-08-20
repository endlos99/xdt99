package net.endlos.xdt99.xas99;

import com.intellij.navigation.ChooseByNameContributor;
import com.intellij.navigation.NavigationItem;
import com.intellij.openapi.project.Project;
import net.endlos.xdt99.xas99.psi.Xas99Labeldef;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

public class Xas99ChooseByNameContributor implements ChooseByNameContributor {
    @NotNull
    @Override
    public String[] getNames(Project project, boolean includeNonProjectItems) {
        List<Xas99Labeldef> labels = Xas99Util.findLabels(project);
        List<String> names = new ArrayList<String>(labels.size());
        for (Xas99Labeldef label : labels) {
            if (label.getName() != null && label.getName().length() > 0) {
                names.add(label.getName());
            }
        }
        return names.toArray(new String[names.size()]);
    }

    @NotNull
    @Override
    public NavigationItem[] getItemsByName(String name, String pattern, Project project, boolean includeNonProjectItems) {
        List<Xas99Labeldef> labels = Xas99Util.findLabels(project, name);
        return labels.toArray(new NavigationItem[labels.size()]);
    }
}
