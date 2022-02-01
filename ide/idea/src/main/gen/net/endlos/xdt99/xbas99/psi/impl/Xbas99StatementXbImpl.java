// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xbas99.psi.Xbas99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xbas99.psi.*;

public class Xbas99StatementXbImpl extends ASTWrapperPsiElement implements Xbas99StatementXb {

  public Xbas99StatementXbImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99Visitor visitor) {
    visitor.visitStatementXb(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xbas99Visitor) accept((Xbas99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xbas99BangComment getBangComment() {
    return findChildByClass(Xbas99BangComment.class);
  }

  @Override
  @Nullable
  public Xbas99SAccept getSAccept() {
    return findChildByClass(Xbas99SAccept.class);
  }

  @Override
  @Nullable
  public Xbas99SLinput getSLinput() {
    return findChildByClass(Xbas99SLinput.class);
  }

  @Override
  @Nullable
  public Xbas99SOnCond getSOnCond() {
    return findChildByClass(Xbas99SOnCond.class);
  }

  @Override
  @Nullable
  public Xbas99SRun getSRun() {
    return findChildByClass(Xbas99SRun.class);
  }

  @Override
  @Nullable
  public Xbas99SSub getSSub() {
    return findChildByClass(Xbas99SSub.class);
  }

  @Override
  @Nullable
  public Xbas99SSubend getSSubend() {
    return findChildByClass(Xbas99SSubend.class);
  }

}
