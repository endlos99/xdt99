package net.endlos.xdt99.xas99;

import com.intellij.lang.refactoring.NamesValidator;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

public class Xas99NamesValidator implements NamesValidator {
    @Override
    public boolean isKeyword(@NotNull final String name, final Project project) {
        return false;
    }

    @Override
    public boolean isIdentifier(@NotNull final String name, final Project project) {
        return name.matches("[A-Za-z_][^@$!,;>:+\\-*/\\^&|~()]*");  // cannot rename into local label!
    }
}
