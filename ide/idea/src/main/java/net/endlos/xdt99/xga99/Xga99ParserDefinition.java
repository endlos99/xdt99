package net.endlos.xdt99.xga99;

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
import net.endlos.xdt99.xga99.parser.Xga99Parser;
import net.endlos.xdt99.xga99.psi.Xga99File;
import net.endlos.xdt99.xga99.psi.Xga99Types;
import org.jetbrains.annotations.NotNull;

public class Xga99ParserDefinition implements ParserDefinition {
    public static final TokenSet WHITE_SPACES = TokenSet.create(TokenType.WHITE_SPACE);
    public static final TokenSet COMMENTS = TokenSet.create(Xga99Types.COMMENT);
    public static final TokenSet STRINGS = TokenSet.create(Xga99Types.OP_TEXT);

    public static final IFileElementType FILE = new IFileElementType(Xga99Language.INSTANCE);

    @Override
    @NotNull
    public Lexer createLexer(Project project) {
        return new Xga99LexerAdapter();
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
        return new Xga99Parser();
    }

    @Override
    @NotNull
    public IFileElementType getFileNodeType() {
        return FILE;
    }

    @Override
    @NotNull
    public PsiFile createFile(@NotNull FileViewProvider viewProvider) {
        return new Xga99File(viewProvider);
    }

    @Override
    @NotNull
    public SpaceRequirements spaceExistenceTypeBetweenTokens(ASTNode left, ASTNode right) {
        return SpaceRequirements.MAY;
    }

    @Override
    @NotNull
    public PsiElement createElement(ASTNode node) {
        return Xga99Types.Factory.createElement(node);
    }
}