package net.endlos.xdt99.xbas99l;

import com.intellij.openapi.fileTypes.SyntaxHighlighter;
import com.intellij.openapi.fileTypes.SyntaxHighlighterFactory;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import org.jetbrains.annotations.NotNull;

public class Xbas99LSyntaxHighlighterFactory extends SyntaxHighlighterFactory {

    @Override
    @NotNull
    public SyntaxHighlighter getSyntaxHighlighter(Project project, VirtualFile virtualFile) {
        return new Xbas99LSyntaxHighlighter();
    }

}
