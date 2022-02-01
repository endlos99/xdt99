package net.endlos.xdt99.xga99r;

import com.intellij.lang.ASTNode;
import com.intellij.lang.ParserDefinition;
import com.intellij.lang.PsiParser;
import com.intellij.lexer.Lexer;
import com.intellij.openapi.project.Project;
import com.intellij.psi.FileViewProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IFileElementType;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xga99r.parser.Xga99RParser;
import net.endlos.xdt99.xga99r.psi.Xga99RTypes;
import net.endlos.xdt99.xga99r.psi.Xga99RFile;
import org.jetbrains.annotations.NotNull;

public class Xga99RParserDefinition implements ParserDefinition {
    public static final TokenSet WHITE_SPACES = TokenSet.create(TokenType.WHITE_SPACE);
    public static final TokenSet COMMENTS = TokenSet.create(Xga99RTypes.COMMENT);
    public static final TokenSet STRINGS = TokenSet.create(Xga99RTypes.OP_TEXT);

    public static final IFileElementType FILE = new IFileElementType(Xga99RLanguage.INSTANCE);

    @Override
    @NotNull
    public Lexer createLexer(Project project) {
        return new Xga99RLexerAdapter();
    }

    @Override
    @NotNull
    public TokenSet getWhitespaceTokens() {
        return WHITE_SPACES;
    }

    @Override
    @NotNull
    public TokenSet getCommentTokens() {
        return COMMENTS;
    }

    @Override
    @NotNull
    public TokenSet getStringLiteralElements() {
        return STRINGS;
    }

    @Override
    @NotNull
    public PsiParser createParser(final Project project) {
        return new Xga99RParser();
    }

    @Override
    @NotNull
    public IFileElementType getFileNodeType() {
        return FILE;
    }

    @Override
    @NotNull
    public PsiFile createFile(@NotNull FileViewProvider viewProvider) {
        return new Xga99RFile(viewProvider);
    }

    @Override
    @NotNull
    public SpaceRequirements spaceExistenceTypeBetweenTokens(ASTNode left, ASTNode right) {
        return SpaceRequirements.MAY;
    }

    @Override
    @NotNull
    public PsiElement createElement(ASTNode node) {
        return Xga99RTypes.Factory.createElement(node);
    }
}