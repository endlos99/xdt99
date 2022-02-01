// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xga99.psi.Xga99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xga99.psi.*;

public class Xga99OpMsImpl extends ASTWrapperPsiElement implements Xga99OpMs {

  public Xga99OpMsImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99Visitor visitor) {
    visitor.visitOpMs(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xga99Visitor) accept((Xga99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xga99OpIndex getOpIndex() {
    return findChildByClass(Xga99OpIndex.class);
  }

  @Override
  @NotNull
  public Xga99Sexpr getSexpr() {
    return findNotNullChildByClass(Xga99Sexpr.class);
  }

}
