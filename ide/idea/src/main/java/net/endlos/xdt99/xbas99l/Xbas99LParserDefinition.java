package net.endlos.xdt99.xbas99l;

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
import net.endlos.xdt99.xbas99l.parser.Xbas99LParser;
import net.endlos.xdt99.xbas99l.psi.Xbas99LTypes;
import net.endlos.xdt99.xbas99l.psi.Xbas99LFile;
import org.jetbrains.annotations.NotNull;

public class Xbas99LParserDefinition implements ParserDefinition{
    public static final TokenSet WHITE_SPACES = TokenSet.create(TokenType.WHITE_SPACE);
    public static final TokenSet COMMENTS = TokenSet.create(Xbas99LTypes.COMMENT);
    public static final TokenSet STRINGS = TokenSet.create(Xbas99LTypes.QSTRING);

    public static final IFileElementType FILE = new IFileElementType(Xbas99LLanguage.INSTANCE);

    @Override
    @NotNull
    public Lexer createLexer(Project project) {
        return new Xbas99LLexerAdapter();
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
        return new Xbas99LParser();
    }

    @Override
    @NotNull
    public IFileElementType getFileNodeType() {
        return FILE;
    }

    @Override
    @NotNull
    public PsiFile createFile(@NotNull FileViewProvider viewProvider) {
        return new Xbas99LFile(viewProvider);
    }

    @Override
    @NotNull
    public SpaceRequirements spaceExistenceTypeBetweenTokens(ASTNode left, ASTNode right) {
        return SpaceRequirements.MAY;
    }

    @Override
    @NotNull
    public PsiElement createElement(ASTNode node) {
        return Xbas99LTypes.Factory.createElement(node);
    }

}