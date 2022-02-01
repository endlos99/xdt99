package net.endlos.xdt99.xbas99;

import com.intellij.lang.refactoring.NamesValidator;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

public class Xbas99NamesValidator implements NamesValidator {

    @Override
    public boolean isKeyword(@NotNull final String name, final Project project) {
        return false;
    }

    @Override
    public boolean isIdentifier(@NotNull final String name, final Project project) {
        return name.matches("[A-Za-z0-9_@\\[\\]\\\\$]+");
    }

}
