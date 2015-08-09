package net.endlos.xdt99.xbas99;

import com.intellij.openapi.fileTypes.SyntaxHighlighter;
import com.intellij.openapi.fileTypes.SyntaxHighlighterFactory;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import net.endlos.xdt99.xbas99.Xbas99SyntaxHighlighter;
import org.jetbrains.annotations.NotNull;

public class Xbas99SyntaxHighlighterFactory extends SyntaxHighlighterFactory {
    @NotNull
    @Override
    public SyntaxHighlighter getSyntaxHighlighter(Project project, VirtualFile virtualFile) {
        return new Xbas99SyntaxHighlighter();
    }
}
