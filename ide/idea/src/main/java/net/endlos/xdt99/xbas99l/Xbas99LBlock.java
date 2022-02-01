package net.endlos.xdt99.xbas99l;

import com.intellij.formatting.Block;
import com.intellij.formatting.Indent;
import com.intellij.formatting.Spacing;
import com.intellij.lang.ASTNode;
import com.intellij.psi.TokenType;
import com.intellij.psi.formatter.common.AbstractBlock;
import com.intellij.psi.tree.IElementType;
import net.endlos.xdt99.xbas99l.psi.Xbas99LTypes;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

import static org.apache.commons.lang.ArrayUtils.contains;

public class Xbas99LBlock extends AbstractBlock {
    private static final IElementType[] allStatementTokens = {
            Xbas99LTypes.W_ACCEPT,
            Xbas99LTypes.W_AND,
            Xbas99LTypes.W_BASE,
            Xbas99LTypes.W_BREAK,
            Xbas99LTypes.W_CALL,
            Xbas99LTypes.W_CLOSE,
            //Xbas99LTypes.W_DATA,  // do not touch
            Xbas99LTypes.W_DEF,
            Xbas99LTypes.W_DELETE,
            Xbas99LTypes.W_DIM,
            Xbas99LTypes.W_DISPLAY,
            Xbas99LTypes.W_ELSE,
            Xbas99LTypes.W_END,
            Xbas99LTypes.W_ERROR,
            Xbas99LTypes.W_FOR,
            Xbas99LTypes.W_GO,
            Xbas99LTypes.W_GOSUB,
            Xbas99LTypes.W_GOTO,
            Xbas99LTypes.W_IF,
            //Xbas99LTypes.W_IMAGE,  // do not touch
            Xbas99LTypes.W_INPUT,  // also clause
            Xbas99LTypes.W_LET,
            Xbas99LTypes.W_LINPUT,
            Xbas99LTypes.W_NEXT,
            Xbas99LTypes.W_NOT,
            Xbas99LTypes.W_ON,
            Xbas99LTypes.W_OPEN,
            Xbas99LTypes.W_OPTION,
            Xbas99LTypes.W_OR,
            Xbas99LTypes.W_PRINT,
            Xbas99LTypes.W_RANDOMIZE,
            Xbas99LTypes.W_READ,
            Xbas99LTypes.W_RETURN,
            Xbas99LTypes.W_RUN,
            Xbas99LTypes.W_STEP,
            Xbas99LTypes.W_STOP,
            Xbas99LTypes.W_SUB,
            Xbas99LTypes.W_SUBEND,
            Xbas99LTypes.W_SUBEXIT,
            Xbas99LTypes.W_THEN,
            Xbas99LTypes.W_TO,
            Xbas99LTypes.W_TRACE,
            Xbas99LTypes.W_UNBREAK,
            Xbas99LTypes.W_UNTRACE,
            Xbas99LTypes.W_WARNING,
            Xbas99LTypes.W_XOR
    };
    private static final IElementType[] allClauseTokens = {
            Xbas99LTypes.W_ALL,  // ACCEPT, DISPLAY
            Xbas99LTypes.W_APPEND,  // OPEN
            Xbas99LTypes.W_AT,  // ACCEPT, DISPLAY
            Xbas99LTypes.W_BEEP,  // ACCEPT, DISPLAY
            Xbas99LTypes.W_DIGIT,  // ACCEPT
//            Xbas99LTypes.W_DISPLAY,  // OPEN (also keyword)
            Xbas99LTypes.W_ERASE,  // ACCEPT, DISPLAY
//            Xbas99LTypes.W_INPUT,  // OPEN (also keyword)
            Xbas99LTypes.W_FIXED,  // OPEN
            Xbas99LTypes.W_INTERNAL,  // OPEN
            Xbas99LTypes.W_NUMERIC,  // ACCEPT
            Xbas99LTypes.W_OUTPUT,  // OPEN
            Xbas99LTypes.W_PERMANENT,  // OPEN
            Xbas99LTypes.W_RELATIVE,  // OPEN
            Xbas99LTypes.W_SEQUENTIAL,  // OPEN
            Xbas99LTypes.W_SIZE,  // ACCEPT, DISPLAY
            Xbas99LTypes.W_UALPHA,  // ACCEPT
            Xbas99LTypes.W_UPDATE,  // OPEN
            Xbas99LTypes.W_USING,  // DISPLAY
            Xbas99LTypes.W_VALIDATE,  // ACCEPT
            Xbas99LTypes.W_VARIABLE  // OPEN
    };
    private static final IElementType[] allTightOpTokens = {
            Xbas99LTypes.OP_LPAREN,
            Xbas99LTypes.OP_COMMA,
            Xbas99LTypes.OP_RPAREN
    };
    private static final IElementType[] allAmbiguousTokens = {
            Xbas99LTypes.W_INPUT,  // statement, open
            Xbas99LTypes.W_DISPLAY  // statement, open
    };

    public Xbas99LBlock(@NotNull ASTNode node) {
        super(node, null, null);
    }

    @Override
    protected List<Block> buildChildren() {
        List<Block> blocks = new ArrayList<>();
        if (myNode.getElementType() == Xbas99LTypes.W_DATA || myNode.getElementType() == Xbas99LTypes.W_IMAGE)
            return blocks;  // do not substructure DATA and IMAGE
        ASTNode child = myNode.getFirstChildNode();
        while (child != null) {
            if (child.getElementType() != TokenType.WHITE_SPACE) {
                if (child.getTextLength() > 0) {  // mostly required for potentially empty PsiErrorElement nodes
                    blocks.add(new Xbas99LBlock(child));
                }
            }
            child = child.getTreeNext();
        }
        return blocks;
    }

    @Override
    public Indent getIndent() {
        if (myNode.getElementType() == Xbas99LTypes.SLIST)
            return Indent.getSpaceIndent(1);
        else if (myNode.getElementType() == Xbas99LTypes.LABELDEF)
            return Indent.getNoneIndent();
        return null;
    }

    @Override
    @Nullable
    public Spacing getSpacing(@Nullable Block child1, @NotNull Block child2) {
        if (child1 instanceof Xbas99LBlock && child2 instanceof Xbas99LBlock) {
            // NOTE: child1 and child2 always have the same parent!
            ASTNode left = ((Xbas99LBlock) child1).getNode();
            ASTNode right = ((Xbas99LBlock) child2).getNode();
            // fixes non-working indent
            if (right.getElementType() == Xbas99LTypes.SLIST) {
                return null;  // handled by indent, but don't set to NoneIndent
            // label definition <-> statement list
            } else if (left.getElementType() == Xbas99LTypes.LABELDEF && right.getElementType() == Xbas99LTypes.SLIST) {
                return spaces(1);
             // statement separator (ignore paren optimization)
            } else if (left.getElementType() == Xbas99LTypes.OP_SEP ||
                    right.getElementType() == Xbas99LTypes.OP_SEP) {
                return spaces(1);
            // ambiguous clauses
            } else if (contains(allAmbiguousTokens, left.getElementType()) &&
                    left.getTreeParent().getElementType() == Xbas99LTypes.S_OPEN &&
                    contains(allTightOpTokens, right.getElementType())) {
                return spaces(0);
            } else if (contains(allAmbiguousTokens, right.getElementType()) &&
                    right.getTreeParent().getElementType() == Xbas99LTypes.S_OPEN &&
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
            } else if (left.getElementType() == Xbas99LTypes.OP_COLON &&
                    right.getElementType() == Xbas99LTypes.OP_COLON) {
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