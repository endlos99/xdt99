package net.endlos.xdt99.xbas99;

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
import net.endlos.xdt99.xbas99.parser.Xbas99Parser;
import net.endlos.xdt99.xbas99.psi.Xbas99File;
import net.endlos.xdt99.xbas99.psi.Xbas99Types;
import org.jetbrains.annotations.NotNull;

public class Xbas99ParserDefinition implements ParserDefinition{
    public static final TokenSet WHITE_SPACES = TokenSet.create(TokenType.WHITE_SPACE);
    public static final TokenSet COMMENTS = TokenSet.create(Xbas99Types.COMMENT);
    public static final TokenSet STRINGS = TokenSet.create(Xbas99Types.QSTRING);

    public static final IFileElementType FILE = new IFileElementType(Xbas99Language.INSTANCE);

    @Override
    @NotNull
    public Lexer createLexer(Project project) {
        return new Xbas99LexerAdapter();
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
        return new Xbas99Parser();
    }

    @Override
    @NotNull
    public IFileElementType getFileNodeType() {
        return FILE;
    }

    @Override
    @NotNull
    public PsiFile createFile(@NotNull FileViewProvider viewProvider) {
        return new Xbas99File(viewProvider);
    }

    @Override
    @NotNull
    public SpaceRequirements spaceExistenceTypeBetweenTokens(ASTNode left, ASTNode right) {
        return SpaceRequirements.MAY;
    }

    @Override
    @NotNull
    public PsiElement createElement(ASTNode node) {
        return Xbas99Types.Factory.createElement(node);
    }

}