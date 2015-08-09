package net.endlos.xdt99.xas99;

import com.intellij.lang.ASTNode;
import com.intellij.lang.Language;
import com.intellij.lang.ParserDefinition;
import com.intellij.lang.PsiParser;
import com.intellij.lexer.FlexAdapter;
import com.intellij.lexer.Lexer;
import com.intellij.openapi.project.Project;
import com.intellij.psi.FileViewProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IFileElementType;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xas99.parser.Xas99Parser;
import net.endlos.xdt99.xas99.psi.Xas99File;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import org.jetbrains.annotations.NotNull;

import java.io.Reader;

public class Xas99ParserDefinition implements ParserDefinition{
    public static final TokenSet WHITE_SPACES = TokenSet.create(TokenType.WHITE_SPACE);
    public static final TokenSet COMMENTS = TokenSet.create(Xas99Types.EOL_COMMENT);
    public static final TokenSet STRINGS = TokenSet.create(Xas99Types.OP_TEXT);

    public static final IFileElementType FILE = new IFileElementType(Language.<Xas99Language>findInstance(Xas99Language.class));

    @NotNull
    @Override
    public Lexer createLexer(Project project) {
        return new FlexAdapter(new Xas99Lexer((Reader) null));
    }

    @NotNull
    public TokenSet getWhitespaceTokens() {
        return WHITE_SPACES;
    }

    @NotNull
    public TokenSet getCommentTokens() {
        return COMMENTS;
    }

    @NotNull
    public TokenSet getStringLiteralElements() {
        return STRINGS;
    }

    @NotNull
    public PsiParser createParser(final Project project) {
        return new Xas99Parser();
    }

    @Override
    public IFileElementType getFileNodeType() {
        return FILE;
    }

    public PsiFile createFile(FileViewProvider viewProvider) {
        return new Xas99File(viewProvider);
    }

    public SpaceRequirements spaceExistanceTypeBetweenTokens(ASTNode left, ASTNode right) {
        return SpaceRequirements.MAY;
    }

    @NotNull
    public PsiElement createElement(ASTNode node) {
        return Xas99Types.Factory.createElement(node);
    }
}