package net.endlos.xdt99.xbas99;

import com.intellij.formatting.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.TokenType;
import com.intellij.psi.formatter.common.AbstractBlock;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99.psi.Xbas99Types;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

import static org.apache.commons.lang.ArrayUtils.contains;

public class Xbas99Block extends AbstractBlock {
    private static final IElementType[] allStatementTokens = {
            Xbas99Types.W_ACCEPT,
            Xbas99Types.W_AND,
            Xbas99Types.W_BASE,
            Xbas99Types.W_BREAK,
            Xbas99Types.W_CALL,
            Xbas99Types.W_CLOSE,
            //Xbas99Types.W_DATA,  // do not touch
            Xbas99Types.W_DEF,
            Xbas99Types.W_DELETE,
            Xbas99Types.W_DIM,
            Xbas99Types.W_DISPLAY,
            Xbas99Types.W_ELSE,
            Xbas99Types.W_END,
            Xbas99Types.W_ERROR,
            Xbas99Types.W_FOR,
            Xbas99Types.W_GO,
            Xbas99Types.W_GOSUB,
            Xbas99Types.W_GOTO,
            Xbas99Types.W_IF,
            //Xbas99Types.W_IMAGE,  // do not touch
            Xbas99Types.W_INPUT,  // also clause
            Xbas99Types.W_LET,
            Xbas99Types.W_LINPUT,
            Xbas99Types.W_NEXT,
            Xbas99Types.W_NOT,
            Xbas99Types.W_ON,
            Xbas99Types.W_OPEN,
            Xbas99Types.W_OPTION,
            Xbas99Types.W_OR,
            Xbas99Types.W_PRINT,
            Xbas99Types.W_RANDOMIZE,
            Xbas99Types.W_READ,
            Xbas99Types.W_RETURN,
            Xbas99Types.W_RUN,
            Xbas99Types.W_STEP,
            Xbas99Types.W_STOP,
            Xbas99Types.W_SUB,
            Xbas99Types.W_SUBEND,
            Xbas99Types.W_SUBEXIT,
            Xbas99Types.W_THEN,
            Xbas99Types.W_TO,
            Xbas99Types.W_TRACE,
            Xbas99Types.W_UNBREAK,
            Xbas99Types.W_UNTRACE,
            Xbas99Types.W_WARNING,
            Xbas99Types.W_XOR
    };
    private static final IElementType[] allClauseTokens = {
            Xbas99Types.W_ALL,  // ACCEPT, DISPLAY
            Xbas99Types.W_APPEND,  // OPEN
            Xbas99Types.W_AT,  // ACCEPT, DISPLAY
            Xbas99Types.W_BEEP,  // ACCEPT, DISPLAY
            Xbas99Types.W_DIGIT,  // ACCEPT
//            Xbas99Types.W_DISPLAY,  // OPEN (also keyword)
            Xbas99Types.W_ERASE,  // ACCEPT, DISPLAY
            Xbas99Types.W_FIXED,  // OPEN
//              Xbas99Types.W_INPUT,  // OPEN (also keyword)
            Xbas99Types.W_INTERNAL,  // OPEN
            Xbas99Types.W_NUMERIC,  // ACCEPT
            Xbas99Types.W_OUTPUT,  // OPEN
            Xbas99Types.W_PERMANENT,  // OPEN
            Xbas99Types.W_RELATIVE,  // OPEN
            Xbas99Types.W_SEQUENTIAL,  // OPEN
            Xbas99Types.W_SIZE,  // ACCEPT, DISPLAY
            Xbas99Types.W_UALPHA,  // ACCEPT
            Xbas99Types.W_UPDATE,  // OPEN
            Xbas99Types.W_USING,  // DISPLAY
            Xbas99Types.W_VALIDATE,  // ACCEPT
            Xbas99Types.W_VARIABLE  // OPEN
    };
    private static final IElementType[] allTightOpTokens = {
            Xbas99Types.OP_LPAREN,
            Xbas99Types.OP_COMMA,
            Xbas99Types.OP_RPAREN
    };
    private static final IElementType[] allAmbiguousTokens = {
            Xbas99Types.W_INPUT,  // statement, open
            Xbas99Types.W_DISPLAY  // statement, open
    };

    public Xbas99Block(@NotNull ASTNode node) {
        super(node, null, null);
    }

    @Override
    protected List<Block> buildChildren() {
        List<Block> blocks = new ArrayList<>();
        if (myNode.getElementType() == Xbas99Types.W_DATA || myNode.getElementType() == Xbas99Types.W_IMAGE)
            return blocks;  // do not substructure DATA and IMAGE
        ASTNode child = myNode.getFirstChildNode();
        while (child != null) {
            if (child.getElementType() != TokenType.WHITE_SPACE) {
                if (child.getTextLength() > 0) {  // mostly required for potentially empty PsiErrorElement nodes
                    blocks.add(new Xbas99Block(child));
                }
            }
            child = child.getTreeNext();
        }
        return blocks;
    }

    @Override
    public Indent getIndent() {
        return Indent.getNoneIndent();
    }

    @Override
    @Nullable
    public Spacing getSpacing(@Nullable Block child1, @NotNull Block child2) {
        if (child1 instanceof Xbas99Block && child2 instanceof Xbas99Block) {
            // NOTE: child1 and child2 always have the same parent!
            ASTNode left = ((Xbas99Block) child1).getNode();
            ASTNode right = ((Xbas99Block) child2).getNode();
            // line number <-> statement list
            if (left.getElementType() == Xbas99Types.LINEDEF && right.getElementType() == Xbas99Types.SLIST) {
                return spaces(1);
            // statement separator (ignore paren optimization)
            } else if (left.getElementType() == Xbas99Types.OP_SEP ||
                    right.getElementType() == Xbas99Types.OP_SEP) {
                return spaces(1);
            // ambiguous clauses
            } else if (contains(allAmbiguousTokens, left.getElementType()) &&
                    left.getTreeParent().getElementType() == Xbas99Types.S_OPEN &&
                    contains(allTightOpTokens, right.getElementType())) {
                return spaces(0);
            } else if (contains(allAmbiguousTokens, right.getElementType()) &&
                    right.getTreeParent().getElementType() == Xbas99Types.S_OPEN &&
                    contains(allTightOpTokens, left.getElementType())) {
                return spaces(0);
            // statement keywords (ignore paren optimization)
            } else if (contains(allStatementTokens, left.getElementType()) ||
                    contains(allStatementTokens, right.getElementType())) {
                return spaces(1);
                // statement clauses (dealing with parents or commas)
            } else if (contains(allClauseTokens, left.getElementType()) && !contains(allTightOpTokens, right.getElementType())) {
                return spaces(1);
            } else if (contains(allClauseTokens, right.getElementType()) && !contains(allTightOpTokens, left.getElementType())) {
                return spaces(1);
            // print : : :
            } else if (left.getElementType() == Xbas99Types.OP_COLON &&
                    right.getElementType() == Xbas99Types.OP_COLON) {
                return spaces(1);
            // everything else has no spaces
            } else {
                return spaces(0);
            }
        }
        return null;
    }

    @Override
    public boolean isLeaf() {
        return myNode.getFirstChildNode() == null;
    }

    private Spacing spaces(int count) {
        return Spacing.createSpacing(count, count, 0, true, 0);
    }

}