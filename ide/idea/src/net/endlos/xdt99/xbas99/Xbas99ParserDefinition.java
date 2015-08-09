package net.endlos.xdt99.xbas99;

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
import net.endlos.xdt99.xbas99.Xbas99Language;
import net.endlos.xdt99.xbas99.Xbas99Lexer;
import net.endlos.xdt99.xbas99.parser.Xbas99Parser;
import net.endlos.xdt99.xbas99.psi.Xbas99File;
import net.endlos.xdt99.xbas99.psi.Xbas99Types;
import org.jetbrains.annotations.NotNull;

import java.io.Reader;

public class Xbas99ParserDefinition implements ParserDefinition{
    public static final TokenSet WHITE_SPACES = TokenSet.create(TokenType.WHITE_SPACE);
    public static final TokenSet COMMENTS = TokenSet.create(Xbas99Types.A_REM);
    public static final TokenSet STRINGS = TokenSet.create(Xbas99Types.QSTRING);

    public static final IFileElementType FILE = new IFileElementType(Language.<Xbas99Language>findInstance(Xbas99Language.class));

    @NotNull
    @Override
    public Lexer createLexer(Project project) {
        return new FlexAdapter(new Xbas99Lexer((Reader) null));
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
        return new Xbas99Parser();
    }

    @Override
    public IFileElementType getFileNodeType() {
        return FILE;
    }

    public PsiFile createFile(FileViewProvider viewProvider) {
        return new Xbas99File(viewProvider);
    }

    public SpaceRequirements spaceExistanceTypeBetweenTokens(ASTNode left, ASTNode right) {
        return SpaceRequirements.MAY;
    }

    @NotNull
    public PsiElement createElement(ASTNode node) {
        return Xbas99Types.Factory.createElement(node);
    }
}